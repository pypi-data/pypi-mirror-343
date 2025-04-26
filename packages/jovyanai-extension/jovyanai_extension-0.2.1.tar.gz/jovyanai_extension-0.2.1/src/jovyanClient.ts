import { JovyanClient } from '@jovyan/client';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

// Default settings
let backendUrl = 'wss://backend.jovyan-ai.com';
let authToken = '';

// Global client instance
let jovyanClientInstance: JovyanClient | null = null;

// Connection state management
let isConnecting = false;
let connectionPromise: Promise<JovyanClient> | null = null;

// Function to initialize settings from the registry
export const initializeClient = async (
  settingRegistry: ISettingRegistry
): Promise<void> => {
  console.debug('Initializing client from settings...');
  try {
    const settings = await settingRegistry.load(
      '@jovyanai/labextension:plugin'
    );

    backendUrl = settings.get('backendUrl').composite as string;
    authToken = settings.get('authToken').composite as string;
    console.debug(`Loaded settings: backendUrl=${backendUrl}, authToken=${authToken ? '***' : '<empty>'}`);

    // No explicit disconnect needed; creating a new instance will let the old one be garbage collected.

    // Create the new client instance but DO NOT connect yet.
    console.debug('Creating new JovyanClient instance.');
    jovyanClientInstance = new JovyanClient(backendUrl, authToken, '');

    // Reset connection state as we have a new instance
    isConnecting = false;
    connectionPromise = null;

    console.debug('JovyanClient instance created (not connected yet).');

  } catch (error) {
    console.error('Failed to load settings or create client instance:', error);
    // Keep the old instance if creation failed? Or set to null? Setting to null seems safer.
    jovyanClientInstance = null;
    isConnecting = false;
    connectionPromise = null;
  }
};

export const getJovyanClient = async (): Promise<JovyanClient> => {
  if (!jovyanClientInstance) {
    // This might happen if initializeClient failed or hasn't run yet.
    // Maybe wait for initialization? Or throw a clearer error.
    console.error('getJovyanClient called before instance was successfully created.');
    throw new Error('JovyanClient instance not available. Initialization might have failed.');
  }

  // If already connected, return immediately.
  if (jovyanClientInstance.isConnected) {
    console.debug('getJovyanClient: Already connected.');
    return jovyanClientInstance;
  }

  // If currently connecting, wait for the existing connection attempt to finish.
  if (isConnecting && connectionPromise) {
    console.debug('getJovyanClient: Connection in progress, waiting...');
    try {
      // Wait for the ongoing connection attempt
      await connectionPromise;
       // Check status again after waiting, as it might have failed
       if (jovyanClientInstance.isConnected) {
          console.debug('getJovyanClient: Waited for connection, now connected.');
          return jovyanClientInstance;
       } else {
          console.warn('getJovyanClient: Waited for connection, but it failed.');
          // Decide whether to retry or throw. Throwing seems safer to avoid loops.
          throw new Error('Connection attempt failed.');
       }
    } catch (error) {
      console.error('getJovyanClient: Error while waiting for connection:', error);
      throw error; // Re-throw the error from the failed connection attempt
    }
  }

  // If not connected and not connecting, start a new connection attempt.
  console.debug('getJovyanClient: Not connected, initiating connection...');
  isConnecting = true;
  const currentInstance = jovyanClientInstance; // Capture instance in case it changes

  connectionPromise = (async () => {
    try {
      await currentInstance.connect();
      // Check if connect() implicitly starts session or if needed explicitly. Assuming connect handles auth/session.
      // If explicit session start is needed:
      // await currentInstance.startSession();
      console.debug('getJovyanClient: Connection and session successful.');
      return currentInstance;
    } catch (error) {
      console.error('getJovyanClient: Failed to connect/start session:', error);
      connectionPromise = null; // Clear promise on failure
      throw error; // Propagate the error
    } finally {
      // Regardless of success or failure, we are no longer in the 'connecting' state
      isConnecting = false;
      console.debug('getJovyanClient: Connection attempt finished.');
      // We don't clear connectionPromise here, it resolves or rejects
    }
  })();

  try {
    await connectionPromise;
    return currentInstance;
  } catch (error) {
    // The error is already logged in the promise handler
    // Rethrow to signal failure to the caller of getJovyanClient
    throw error;
  }
};

export const clientIsConnected = (): boolean => {
  // Use optional chaining in case instance is null
  return jovyanClientInstance?.isConnected ?? false;
};
