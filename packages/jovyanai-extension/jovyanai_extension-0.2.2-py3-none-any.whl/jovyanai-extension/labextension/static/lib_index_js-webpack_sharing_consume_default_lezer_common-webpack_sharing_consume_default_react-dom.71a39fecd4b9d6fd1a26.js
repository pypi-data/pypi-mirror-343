"use strict";
(self["webpackChunk_jovyanai_labextension"] = self["webpackChunk_jovyanai_labextension"] || []).push([["lib_index_js-webpack_sharing_consume_default_lezer_common-webpack_sharing_consume_default_react-dom"],{

/***/ "./lib/authReminder/authReminder.js":
/*!******************************************!*\
  !*** ./lib/authReminder/authReminder.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AuthReminder: () => (/* binding */ AuthReminder)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../jovyanClient */ "./lib/jovyanClient.js");

// Import real client functions

/**
 * A React component prompting the user for an auth token
 * and attempting to save it and establish a connection.
 */
const AuthReminder = ({ settingRegistry, onConnected, onCancel }) => {
    const [token, setToken] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [isLoading, setIsLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const handleSubmit = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async (event) => {
        event.preventDefault();
        setIsLoading(true);
        setError(null);
        try {
            // 1. Validate token (basic check)
            if (!token.trim()) {
                throw new Error('Token cannot be empty.');
            }
            // 2. Save the token to settings
            await settingRegistry.set('@jovyanai/labextension:plugin', 'authToken', token);
            console.debug('Auth token setting updated.');
            // 3. Re-initialize the client with the new settings (including the token)
            //    This function reads settings and attempts connection.
            const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_1__.getJovyanClient)();
            try {
                // Explicitly check connection status AFTER attempting to connect
                if (client.isConnected) {
                    console.debug('Connection successful.');
                    if (onConnected) {
                        onConnected();
                    }
                }
                else {
                    // This case might happen if connect() resolves but connection fails silently
                    // or if the status check has latency. Provide feedback.
                    console.error('Connection attempt finished, but client is not connected.');
                    throw new Error('Connection failed. Please verify your token and network.');
                }
            }
            catch (err) {
                console.error('Failed to connect:', err);
                // Keep the original error message if available, otherwise provide a default
                const connectionError = err.message && err.message.includes('Connection failed')
                    ? err.message
                    : 'Connection failed. Please check your token and network.';
                throw new Error(connectionError);
            }
        }
        catch (err) {
            console.error('Failed to save token or connect:', err);
            setError(err.message || 'An unexpected error occurred.');
        }
        finally {
            setIsLoading(false);
        }
    }, [token, settingRegistry, onConnected]);
    // Basic styling, can be replaced with JupyterLab UI components later
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-AuthReminder-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h4", null, "Please enter your authentication token to proceed:"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
            "Your token is available in your Jovyan AI account ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { href: "https://jovyan-ai.com/account" }, "here"),
            "."),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: handleSubmit, className: "jp-AuthReminder-form" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "password", value: token, onChange: (e) => setToken(e.target.value), placeholder: "Enter your token", disabled: isLoading, className: "jp-AuthReminder-input" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit", disabled: isLoading || !token.trim(), className: "jp-AuthReminder-button jp-AuthReminder-button-submit" }, isLoading ? 'Connecting...' : 'Connect'),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: onCancel, disabled: isLoading, className: "jp-AuthReminder-button" }, "Cancel")),
        error && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "jp-AuthReminder-error" },
            "Error: ",
            error))));
};


/***/ }),

/***/ "./lib/cellOps/components/ActivateCellButton.js":
/*!******************************************************!*\
  !*** ./lib/cellOps/components/ActivateCellButton.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// button in the top right corner of the cell to activate AI commands

const ActivateCellButton = ({ onClick, text }) => {
    // Text is Generate code on new cell or Change code in cell with some existing code
    const [tooltipVisible, setTooltipVisible] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    // get shortcut keybinding by checking if Mac
    const isMac = /Mac/i.test(navigator.userAgent);
    const shortcut = isMac ? '⌘K' : '^K';
    const shortcutText = isMac ? 'Cmd+K' : 'Ctrl+K';
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-ai-button-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jv-cell-ai-button", title: `Generate code ${shortcut}`, onClick: onClick, onMouseEnter: () => setTooltipVisible(true), onMouseLeave: () => setTooltipVisible(false) },
            text,
            " ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.8em' } }, shortcut)),
        tooltipVisible && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-ai-tooltip" },
            "Open the prompt box to instruct AI (",
            shortcutText,
            ")"))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ActivateCellButton);


/***/ }),

/***/ "./lib/cellOps/components/CellPromptInput.js":
/*!***************************************************!*\
  !*** ./lib/cellOps/components/CellPromptInput.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _monaco_editor_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @monaco-editor/react */ "webpack/sharing/consume/default/@monaco-editor/react/@monaco-editor/react");
/* harmony import */ var _monaco_editor_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_monaco_editor_react__WEBPACK_IMPORTED_MODULE_1__);
// AI prompt input component with a text input and a button to send the prompt to AI


const Button = ({ onClick, disabled = false, className, children }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: onClick, disabled: disabled, className: className || 'jv-default-button', style: {
            cursor: disabled ? 'not-allowed' : 'pointer',
            opacity: disabled ? 0.6 : 1
        } }, children));
};
const InputComponent = ({ isEnabled, placeholderEnabled, placeholderDisabled, initialInput, onSubmit, onCancel }) => {
    const [editorValue, setEditorValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initialInput || '');
    const editorRef = react__WEBPACK_IMPORTED_MODULE_0___default().useRef(null);
    const handleEditorChange = (value) => {
        if (value !== undefined) {
            setEditorValue(value);
        }
    };
    const handleEditorMount = (editor, monaco) => {
        editorRef.current = editor;
        // Add event listeners
        editor.onKeyDown(async (event) => {
            // Check if autocomplete widget is visible
            const isAutocompleteWidgetVisible = () => {
                const editorElement = editor.getContainerDomNode();
                const suggestWidget = editorElement.querySelector('.editor-widget.suggest-widget.visible');
                return (suggestWidget !== null &&
                    suggestWidget.getAttribute('monaco-visible-content-widget') === 'true');
            };
            if (isAutocompleteWidgetVisible()) {
                // Let Monaco handle the key events when autocomplete is open
                return;
            }
            if (event.code === 'Escape') {
                event.preventDefault();
                onCancel();
            }
            if (event.code === 'Enter') {
                event.preventDefault();
                if (event.shiftKey) {
                    editor.trigger('keyboard', 'type', { text: '\n' });
                }
                else {
                    handleSubmit();
                }
            }
        });
        editor.focus();
    };
    const handleSubmit = () => {
        var _a;
        // Get the most current value directly from the editor
        const currentValue = ((_a = editorRef.current) === null || _a === void 0 ? void 0 : _a.getValue()) || editorValue;
        if (currentValue.trim() === '') {
            return;
        }
        onSubmit(currentValue);
        setEditorValue('');
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-ai-input-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-ai-input-editor" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_monaco_editor_react__WEBPACK_IMPORTED_MODULE_1__.Editor, { defaultLanguage: "markdown", theme: document.body.getAttribute('data-jp-theme-light') === 'true'
                    ? 'vs'
                    : 'vs-dark', value: editorValue, onChange: handleEditorChange, onMount: handleEditorMount, options: {
                    minimap: { enabled: false },
                    lineNumbers: 'off',
                    glyphMargin: false,
                    folding: false,
                    wordWrap: 'on',
                    wrappingIndent: 'same',
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    readOnly: !isEnabled,
                    placeholder: isEnabled ? placeholderEnabled : placeholderDisabled
                } })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-ai-input-buttons" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Button, { onClick: handleSubmit, disabled: !isEnabled || editorValue.trim() === '', className: "jv-cell-ai-input-submit-button" },
                "Submit",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.7em', marginLeft: '5px' } }, "Enter")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Button, { onClick: onCancel, className: "jv-cell-ai-input-cancel-button" },
                "Cancel",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.7em', marginLeft: '5px' } }, "Escape")))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (InputComponent);


/***/ }),

/***/ "./lib/cellOps/components/DiffReview.js":
/*!**********************************************!*\
  !*** ./lib/cellOps/components/DiffReview.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DiffReview: () => (/* binding */ DiffReview)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @codemirror/view */ "webpack/sharing/consume/default/@codemirror/view");
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_codemirror_view__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _codemirror_merge__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @codemirror/merge */ "webpack/sharing/consume/default/@codemirror/merge/@codemirror/merge");
/* harmony import */ var _codemirror_merge__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_codemirror_merge__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _codemirror_lang_python__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @codemirror/lang-python */ "./node_modules/@codemirror/lang-python/dist/index.js");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _DiffReviewButtons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./DiffReviewButtons */ "./lib/cellOps/components/DiffReviewButtons.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);









function applyDiffToEditor(editor, original, modified, isNewCodeGeneration = false) {
    // This function
    const extensions = [
        (0,_codemirror_lang_python__WEBPACK_IMPORTED_MODULE_6__.python)(),
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__.jupyterTheme,
        _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.EditorView.editable.of(false),
        _codemirror_state__WEBPACK_IMPORTED_MODULE_2__.EditorState.readOnly.of(true),
        (0,_codemirror_view__WEBPACK_IMPORTED_MODULE_1__.highlightSpecialChars)()
    ];
    if (!isNewCodeGeneration) {
        extensions.push((0,_codemirror_merge__WEBPACK_IMPORTED_MODULE_3__.unifiedMergeView)({
            original: original,
            mergeControls: false,
            gutter: false
        }));
    }
    // Create a new EditorView with the diff content
    const newView = new _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.EditorView({
        state: _codemirror_state__WEBPACK_IMPORTED_MODULE_2__.EditorState.create({
            doc: modified,
            extensions: extensions
        }),
        parent: editor.editor.dom
    });
    // Hide the original editor view
    editor.editor.dom.classList.add('hidden-editor');
    // Add a class for new code generation
    if (isNewCodeGeneration) {
        newView.dom.classList.add('new-code-generation');
    }
    // add a streaming-now class to the new view
    newView.dom.classList.add('streaming-now');
    // Append the new view to the same parent as the original editor
    editor.host.appendChild(newView.dom);
    return newView;
}
const DiffReview = ({ activeCell, oldCode, generateCodeStream, acceptCodeHandler, rejectCodeHandler, editPromptHandler, acceptAndRunHandler, prompt, // Destructure prompt
retryHandler // Destructure retryHandler
 }) => {
    const [diffView, setDiffView] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [stream, setStream] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [newCode, setNewCode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [streamingDone, setStreamingDone] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [statusText, setStatusText] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('Thinking...');
    const buttonsRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [isCancelled, setIsCancelled] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [isServerError, setIsServerError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false); // Add server error state
    const timeoutId = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null); // Use ReturnType<typeof setTimeout>
    const firstChunkReceived = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(false); // Add ref to track first chunk
    // Create the diff view once the active cell and old code are available.
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (activeCell && oldCode !== undefined) {
            const editor = activeCell.editor;
            const initialDiffView = applyDiffToEditor(editor, oldCode, oldCode, oldCode.trim() === '' // flag for new code generation
            );
            setDiffView(initialDiffView);
        }
        activeCell.node.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }, [activeCell, oldCode]);
    // Start the code generation stream.
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const initiateStream = async () => {
            try {
                setIsServerError(false); // Reset server error state on new attempt
                setStatusText('Thinking...'); // Reset status text
                setNewCode(''); // Reset new code
                setStreamingDone(false); // Reset streaming done state
                firstChunkReceived.current = false; // Reset first chunk flag
                const codeStream = generateCodeStream;
                setStream(codeStream);
            }
            catch (error) {
                console.error('Error generating code stream:', error);
                setStreamingDone(true);
                setIsServerError(true); // Set server error state
                // Don't clean up here, let the status text show the error and Try Again button
                setStatusText('Error generating code. Please try again.');
            }
        };
        initiateStream();
        // Dependency array includes generateCodeStream to re-run if it changes (e.g., on retry)
    }, [generateCodeStream]);
    // Accumulate code from the stream.
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (stream) {
            const accumulate = async () => {
                firstChunkReceived.current = false; // Reset flag
                setIsServerError(false); // Reset server error state at start of accumulation
                // Set timeout for the first chunk
                timeoutId.current = setTimeout(() => {
                    if (!firstChunkReceived.current) {
                        setStreamingDone(true); // Stop further processing
                        setIsServerError(true); // Set server error state for timeout
                        setStatusText('Error: Server took too long to respond. Please try again.');
                        // Don't clean up here, let the error message show
                    }
                }, 120000); // 2 minutes timeout
                try {
                    for await (const chunk of stream) {
                        // Clear timeout once the first chunk arrives
                        if (!firstChunkReceived.current) {
                            firstChunkReceived.current = true;
                            if (timeoutId.current) {
                                clearTimeout(timeoutId.current);
                                timeoutId.current = null;
                            }
                            setStatusText('Writing...'); // Update status once streaming starts
                        }
                        setNewCode(prevCode => prevCode + chunk);
                    }
                    setStreamingDone(true);
                    if (firstChunkReceived.current) {
                        // Only clear status if we actually received something
                        setStatusText('');
                    }
                    else if (!isServerError) {
                        // If stream ended without chunks and no timeout error, maybe empty response?
                        setStatusText('Received empty response.'); // Or handle as appropriate
                        setIsServerError(true); // Consider empty response a server issue?
                    }
                }
                catch (error) {
                    console.error('Error processing stream:', error);
                    setStreamingDone(true);
                    setIsServerError(true); // Assume processing errors are server-related for retry
                    // Check if timeout already triggered the error message
                    if (!timeoutId.current && firstChunkReceived.current) {
                        setStatusText('Error processing stream.');
                    }
                    else if (!firstChunkReceived.current && !timeoutId.current) {
                        // If timeout hasn't fired and we haven't received a chunk, maybe network error before timeout
                        setStatusText('Error starting stream.');
                    } // else timeout message is already set or will be set
                }
                finally {
                    // Ensure timeout is cleared if stream ends or errors out before timeout fires
                    if (timeoutId.current) {
                        clearTimeout(timeoutId.current);
                        timeoutId.current = null;
                    }
                }
            };
            accumulate();
        }
        // Cleanup function to clear timeout if component unmounts or stream changes
        return () => {
            if (timeoutId.current) {
                clearTimeout(timeoutId.current);
                timeoutId.current = null;
            }
        };
    }, [stream]); // Re-run if the stream object itself changes (e.g., on retry)
    // When streaming is complete, finalize the diff view by applying fixed code.
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (streamingDone && diffView) {
            diffView.dom.classList.remove('streaming-now');
            diffView.dispatch({
                changes: {
                    from: 0,
                    to: diffView.state.doc.length,
                    insert: newCode
                }
            });
        }
    }, [streamingDone, diffView, newCode]);
    // when streming is done, scroll the button container into view
    // useEffect(() => {
    //   if (streamingDone && buttonsRef.current) {
    //     buttonsRef.current.scrollIntoView({
    //       behavior: 'smooth',
    //       block: 'center'
    //     });
    //   }
    // }, [streamingDone]);
    // Continuously update the diff view while new code arrives.
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        var _a;
        if (!streamingDone && activeCell && diffView) {
            const oldCodeLines = oldCode.split('\n');
            const newCodeLines = newCode.split('\n');
            if (newCodeLines.length > 1) {
                let diffCode = '';
                if (newCodeLines.length < oldCodeLines.length) {
                    diffCode = [
                        ...newCodeLines.slice(0, -1),
                        oldCodeLines[newCodeLines.length - 1] + '\u200B',
                        ...oldCodeLines.slice(newCodeLines.length)
                    ].join('\n');
                }
                else {
                    diffCode = newCode.split('\n').slice(0, -1).join('\n');
                }
                diffView.dispatch({
                    changes: {
                        from: 0,
                        to: diffView.state.doc.length,
                        insert: diffCode
                    }
                });
                // Optionally, mark the last changed line.
                const changedLines = diffView.dom.querySelectorAll('.cm-changedLine');
                if (changedLines.length > 0) {
                    (_a = changedLines[changedLines.length - 1].previousElementSibling) === null || _a === void 0 ? void 0 : _a.classList.add('hidden-diff');
                }
            }
        }
    }, [newCode, streamingDone, activeCell, diffView, oldCode]);
    const cleanUp = () => {
        // remove the diff review and restore the original editor
        const diffReviewContainer = diffView === null || diffView === void 0 ? void 0 : diffView.dom;
        if (diffReviewContainer) {
            diffReviewContainer.remove();
        }
        const editor = activeCell.editor;
        editor.editor.dom.classList.remove('hidden-editor');
        // remove the buttons container
        const buttonsContainer = buttonsRef.current;
        if (buttonsContainer) {
            buttonsContainer.remove();
        }
    };
    const onAcceptAndRun = () => {
        acceptAndRunHandler(newCode);
        cleanUp();
    };
    const onAccept = () => {
        acceptCodeHandler(newCode);
        cleanUp();
    };
    const onReject = () => {
        rejectCodeHandler();
        cleanUp();
    };
    const onEditPrompt = () => {
        editPromptHandler(newCode);
        cleanUp();
    };
    const onCancel = () => {
        setIsCancelled(true);
        setStreamingDone(true);
        setStatusText('');
        setStream(null);
        rejectCodeHandler();
        cleanUp();
    };
    const handleRetry = () => {
        // No need to call cleanUp here as the parent will re-render/replace this instance
        retryHandler();
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        statusText && !isCancelled && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "status-container" },
            !streamingDone && !isServerError && !isCancelled && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "spinner-container" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "spinner-border" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "cancel-button", onClick: onCancel, title: "Cancel request" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.stopIcon.react, null)))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "status-element" }, statusText),
            isServerError && streamingDone && !isCancelled && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: handleRetry, title: "Retry Request" }, "Try Again")))),
        diffView &&
            streamingDone &&
            !isCancelled &&
            !isServerError && ( // Only show buttons if no server error
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_DiffReviewButtons__WEBPACK_IMPORTED_MODULE_7__.ButtonsContainer, { buttonsRef: buttonsRef, onAcceptAndRun: onAcceptAndRun, onAccept: onAccept, onReject: onReject, onEditPrompt: onEditPrompt }))));
};


/***/ }),

/***/ "./lib/cellOps/components/DiffReviewButtons.js":
/*!*****************************************************!*\
  !*** ./lib/cellOps/components/DiffReviewButtons.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ButtonsContainer: () => (/* binding */ ButtonsContainer)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

// import posthog from 'posthog-js';
const ButtonWithTooltip = ({ onClick, className, text, shortcut, tooltip }) => {
    const [showTooltip, setShowTooltip] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-diff-review-button-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: onClick, className: className, onMouseEnter: () => setShowTooltip(true), onMouseLeave: () => setShowTooltip(false), title: `${text} ${shortcut}` },
            text,
            " ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.7em' } }, shortcut)),
        showTooltip && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "tooltip" },
            tooltip,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            "Shortcut: ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null, shortcut)))));
};
const ButtonsContainer = ({ buttonsRef, onAcceptAndRun, onAccept, onReject
// onEditPrompt
 }) => {
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (buttonsRef.current) {
            buttonsRef.current.focus({ preventScroll: true });
        }
    }, []);
    // const isMac = /Mac/i.test(navigator.userAgent);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-diff-review-buttons-container", tabIndex: 0, ref: buttonsRef, onKeyDown: event => {
            if (event.key === 'Enter') {
                event.preventDefault();
                if (!event.shiftKey && !(event.metaKey || event.ctrlKey)) {
                    const acceptButton = document.querySelector('.accept-button');
                    acceptButton.click();
                }
                else if (event.shiftKey) {
                    const acceptAndRunButton = document.querySelector('.accept-and-run-button');
                    acceptAndRunButton.click();
                }
            }
            else if (event.key === 'm' && (event.metaKey || event.ctrlKey)) {
                event.preventDefault();
                const editPromptButton = document.querySelector('.edit-prompt-button');
                editPromptButton.click();
            }
            else if (event.key === 'Escape') {
                event.preventDefault();
                const rejectButton = document.querySelector('.reject-button');
                rejectButton.click();
            }
        }, onBlur: () => {
            // Refocus the container when it loses focus
            if (buttonsRef.current) {
                buttonsRef.current.focus({ preventScroll: true });
            }
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ButtonWithTooltip, { onClick: onAcceptAndRun, className: "accept-and-run-button", text: "Accept & Run", shortcut: "Shift + Enter", tooltip: "Accept the changes and run the code in the current cell." }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ButtonWithTooltip, { onClick: onReject, className: "reject-button", text: "Reject", shortcut: "Escape", tooltip: "Reject the changes and revert to the original code." }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ButtonWithTooltip, { onClick: onAccept, className: "accept-button", text: "Accept", shortcut: "Enter", tooltip: "Accept the changes and keep the code in the current cell." })));
};


/***/ }),

/***/ "./lib/cellOps/components/FixErrorButton.js":
/*!**************************************************!*\
  !*** ./lib/cellOps/components/FixErrorButton.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// button in the top right corner of the cell to activate AI commands

const FixErrorButton = ({ onClick, text }) => {
    // Text is Generate code on new cell or Change code in cell with some existing code
    const [tooltipVisible, setTooltipVisible] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    // get shortcut keybinding by checking if Mac
    //   const isMac = /Mac/i.test(navigator.userAgent);
    const shortcut = '⇧F';
    const shortcutText = 'Shift+F';
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-fix-error-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jv-cell-fix-error-button", title: `Fix Error ${shortcut}`, onClick: onClick, onMouseEnter: () => setTooltipVisible(true), onMouseLeave: () => setTooltipVisible(false) },
            text,
            " ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.8em' } }, shortcut)),
        tooltipVisible && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jv-cell-fix-error-tooltip" },
            "Fix this error with AI (",
            shortcutText,
            ")"))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FixErrorButton);


/***/ }),

/***/ "./lib/cellOps/jovyanCellController.js":
/*!*********************************************!*\
  !*** ./lib/cellOps/jovyanCellController.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JovyanCellController: () => (/* binding */ JovyanCellController)
/* harmony export */ });
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../jovyanClient */ "./lib/jovyanClient.js");
/* harmony import */ var _components_ActivateCellButton__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/ActivateCellButton */ "./lib/cellOps/components/ActivateCellButton.js");
/* harmony import */ var _components_FixErrorButton__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/FixErrorButton */ "./lib/cellOps/components/FixErrorButton.js");
/* harmony import */ var _components_CellPromptInput__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/CellPromptInput */ "./lib/cellOps/components/CellPromptInput.js");
/* harmony import */ var _components_DiffReview__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/DiffReview */ "./lib/cellOps/components/DiffReview.js");
/* harmony import */ var _handleCodeGeneration__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../handleCodeGeneration */ "./lib/handleCodeGeneration.js");
/* harmony import */ var _utils_authDialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../utils/authDialog */ "./lib/utils/authDialog.js");









class JovyanCellController {
    constructor(cell, notebookController) {
        this.addCellActivateButton = () => {
            // remove all existing buttons
            this.removeAllActivateButtons();
            // if cell has code, show generate code button
            // if cell has no code, show change code button
            let text = 'Generate';
            if (this._cell.model.type === 'code') {
                const codeCellModel = this._cell.model;
                if (codeCellModel.sharedModel.source) {
                    text = 'Modify';
                }
            }
            const buttonContainer = document.createElement('div');
            const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_0__.createRoot)(buttonContainer);
            const cellNode = this._cell.node;
            const handleClick = () => {
                this.addPromptInput();
                buttonContainer.remove();
            };
            const button = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_ActivateCellButton__WEBPACK_IMPORTED_MODULE_2__["default"], {
                onClick: handleClick,
                text: text
            });
            root.render(button);
            cellNode.appendChild(buttonContainer);
            // add event listener to the cell to catch the keydown event
            if (!cellNode.hasAttribute('jv-activate-listener')) {
                cellNode.addEventListener('keydown', event => {
                    if (event.key === 'k' && event.metaKey) {
                        event.preventDefault();
                        handleClick();
                    }
                });
                // Mark the cell as having the listener attached
                cellNode.setAttribute('jv-activate-listener', 'true');
            }
        };
        this._cell = cell;
        this._notebookController = notebookController;
    }
    removeAllActivateButtons() {
        const button = document.querySelector('.jv-cell-ai-button-container');
        if (button) {
            button.remove();
        }
    }
    removeCellActivateButton() {
        const button = this._cell.node.querySelector('.jv-cell-ai-button-container');
        if (button) {
            button.remove();
        }
    }
    activate() {
        // console.debug('Activating cell', this._cell.node);
        // remove all existing buttons
        this.removeAllActivateButtons();
        // add the button to the cell
        this.addCellActivateButton();
        this.addFixErrorButton();
    }
    _checkIsErrorCell() {
        if (this._cell.model.type !== 'code') {
            return false;
        }
        const codeCellModel = this._cell.model;
        if (codeCellModel.sharedModel.outputs.length === 0) {
            return false;
        }
        for (const output of codeCellModel.sharedModel.outputs) {
            if (output.output_type === 'error') {
                return true;
            }
        }
        return false;
    }
    addFixErrorButton() {
        if (this._cell.model.type !== 'code') {
            return;
        }
        // console.debug('Adding fix error button', this._cell.node);
        // check if error button already exists
        const errorButton = this._cell.node.querySelector('.jv-cell-fix-error-container');
        if (errorButton) {
            // remove the error button
            errorButton.remove();
        }
        // add button to cell output node
        const cellNode = this._cell.node;
        const outputArea = cellNode.querySelector('.jp-Cell-outputArea');
        if (!outputArea) {
            return;
        }
        if (!this._checkIsErrorCell()) {
            return;
        }
        const buttonContainer = document.createElement('div');
        const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_0__.createRoot)(buttonContainer);
        const handleClick = async () => {
            if (!this._checkIsErrorCell()) {
                return;
            }
            try {
                const codeStream = await this.createCodeStream('Fix the error in the current cell.');
                if (!codeStream) {
                    console.debug('Fix error cancelled due to auth.');
                    this.activate();
                    return;
                }
                this.addDiffReview(codeStream, 'Fix the error in the current cell.');
                buttonContainer.remove();
            }
            catch (error) {
                console.error('Error during fix error action:', error);
                this.activate();
            }
        };
        const button = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_FixErrorButton__WEBPACK_IMPORTED_MODULE_3__["default"], {
            onClick: handleClick,
            text: 'Fix Error'
        });
        root.render(button);
        outputArea.appendChild(buttonContainer);
        // Add event listener only if it doesn't exist already
        // Use a custom attribute to check if the listener is already attached
        if (!cellNode.hasAttribute('jv-fix-error-listener')) {
            cellNode.addEventListener('keydown', (event) => {
                if (event.key === 'F' && event.shiftKey) {
                    event.preventDefault();
                    handleClick();
                }
            });
            // Mark the cell as having the listener attached
            cellNode.setAttribute('jv-fix-error-listener', 'true');
        }
    }
    addPromptInput() {
        const cellNode = this._cell.node;
        if (cellNode.querySelector('.jv-cell-ai-input-container')) {
            console.debug('Input container already exists, skipping add.');
            return;
        }
        console.debug('Creating input container for cell:', this._cell.id);
        const inputContainer = document.createElement('div');
        inputContainer.style.position = 'relative';
        inputContainer.style.marginTop = '10px';
        inputContainer.tabIndex = -1;
        inputContainer.style.outline = 'none';
        const inputComponent = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_CellPromptInput__WEBPACK_IMPORTED_MODULE_4__["default"], {
            isEnabled: true,
            placeholderEnabled: 'Ask Jovyan',
            placeholderDisabled: 'Input disabled',
            onSubmit: async (prompt) => {
                try {
                    const codeStream = await this.createCodeStream(prompt);
                    if (!codeStream) {
                        console.debug('Code generation cancelled due to auth.');
                        this.removePromptInput();
                        this.activate();
                        return;
                    }
                    this.addDiffReview(codeStream, prompt);
                    this.removePromptInput();
                }
                catch (error) {
                    console.error('Error during prompt submission:', error);
                    this.activate();
                }
            },
            onCancel: () => {
                console.debug('Prompt cancelled');
                inputContainer.remove();
                this.addCellActivateButton();
            }
        });
        const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_0__.createRoot)(inputContainer);
        root.render(inputComponent);
        this._notebookController.addElementAfterCellInput(this._cell, inputContainer);
        // Use setTimeout to ensure the element is rendered and focusable
        setTimeout(() => {
            try {
                inputContainer.focus();
            }
            catch (e) {
                console.error('Error focusing inputContainer:', e);
            }
            try {
                inputContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            catch (e) {
                console.error('Error scrolling inputContainer:', e);
            }
        }, 0); // 0ms delay
    }
    removePromptInput() {
        const inputContainer = this._cell.node.querySelector('.jv-cell-ai-input-container');
        if (inputContainer) {
            inputContainer.remove();
        }
    }
    async createCodeStream(prompt) {
        if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_5__.clientIsConnected)()) {
            console.debug('Jovyan client not connected. Prompting for auth.');
            const userCancelled = await (0,_utils_authDialog__WEBPACK_IMPORTED_MODULE_6__.showAuthReminderDialog)(this._notebookController.settingRegistry);
            if (userCancelled) {
                console.debug('Auth dialog cancelled by user.');
                return null;
            }
            if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_5__.clientIsConnected)()) {
                console.warn("Auth dialog closed but client still not connected.");
                return null;
            }
        }
        try {
            const codeStream = (0,_handleCodeGeneration__WEBPACK_IMPORTED_MODULE_7__.setupCodeGenerationStream)({
                currentCell: this._cell,
                previousCells: this._notebookController.getPreviousCells(this._cell),
                nextCells: this._notebookController.getNextCells(this._cell),
                userInput: prompt,
                language: this._notebookController.getLanguage()
            });
            return codeStream;
        }
        catch (error) {
            console.error('Error during code stream setup:', error);
            this.activate();
            return null;
        }
    }
    addDiffReview(codeStream, prompt) {
        const diffReviewContainer = document.createElement('div');
        const existingContainer = this._cell.node.querySelector('.jv-diff-review-container');
        if (existingContainer) {
            existingContainer.remove();
        }
        diffReviewContainer.className = 'jv-diff-review-container';
        const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_0__.createRoot)(diffReviewContainer);
        const retryHandler = async () => {
            // console.debug(`Retrying prompt: ${prompt}`);
            const oldContainer = this._cell.node.querySelector('.jv-diff-review-container');
            if (oldContainer) {
                oldContainer.remove();
            }
            try {
                const newCodeStream = await this.createCodeStream(prompt);
                if (newCodeStream) {
                    this.addDiffReview(newCodeStream, prompt);
                }
                else {
                    console.debug('Retry cancelled or failed.');
                    this.activate();
                }
            }
            catch (error) {
                console.error('Error during retry:', error);
                this.activate();
            }
        };
        const diffReviewComponent = react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_DiffReview__WEBPACK_IMPORTED_MODULE_8__.DiffReview, {
            activeCell: this._cell,
            oldCode: this._cell.model.sharedModel.source,
            generateCodeStream: codeStream,
            prompt: prompt,
            retryHandler: retryHandler,
            acceptCodeHandler: (code) => {
                this._notebookController.writeCodeInCell(this._cell, code);
                this.activate();
            },
            rejectCodeHandler: () => {
                this.activate();
            },
            editPromptHandler: (code) => {
                this._notebookController.writeCodeInCell(this._cell, code);
                this.addPromptInput();
            },
            acceptAndRunHandler: (code) => {
                this._notebookController.writeCodeInCell(this._cell, code);
                this._notebookController.runCell(this._cell);
                this.activate();
                this._notebookController.insertCell(this._notebookController.currentCellIndex + 1);
            }
        });
        root.render(diffReviewComponent);
        this._notebookController.addElementAfterCellInput(this._cell, diffReviewContainer);
    }
}


/***/ }),

/***/ "./lib/chatAssistant/ChatContextProvider.js":
/*!**************************************************!*\
  !*** ./lib/chatAssistant/ChatContextProvider.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatContextProvider: () => (/* binding */ ChatContextProvider),
/* harmony export */   useChatContext: () => (/* binding */ useChatContext)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../context/NotebookControllerContext */ "./lib/context/NotebookControllerContext.js");
/* harmony import */ var _chatContextController__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./chatContextController */ "./lib/chatAssistant/chatContextController.js");
'use client'; // Add if this provider is used in client components

 // Check path
 // Import the controller class
// Create the context
const ChatContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
// --- Context Provider Component ---
const ChatContextProvider = ({ children }) => {
    const notebookController = (0,_context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_1__.useNotebookController)();
    const [activeContexts, setActiveContexts] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [currentNotebookInContext, setCurrentNotebookInContext] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const [currentNotebookFileName, setCurrentNotebookFileName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    // Create a stable instance of the controller logic class
    // Make sure ChatContextController is imported correctly
    const controller = (0,react__WEBPACK_IMPORTED_MODULE_0__.useMemo)(() => new _chatContextController__WEBPACK_IMPORTED_MODULE_2__.ChatContextController(notebookController), [notebookController]);
    // Track current notebook filename
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        // Check if notebookController and its tracker exist
        if (notebookController && notebookController._notebookTracker) {
            const tracker = notebookController._notebookTracker;
            // Define the handler function - now async and waits for context ready
            const updateFilename = async (sender, panel) => {
                var _a;
                let filename = '';
                if (panel) {
                    try {
                        // console.debug(
                        //   'Signal received. Waiting for panel context to be ready...'
                        // );
                        await panel.context.ready; // Wait for the context
                        // console.debug('Panel context is ready.');
                        // Now get the path
                        const path = (_a = panel.context.contentsModel) === null || _a === void 0 ? void 0 : _a.path;
                        if (path) {
                            const parts = path.split('/');
                            filename = parts[parts.length - 1];
                        }
                        // console.debug(
                        //   'Panel path after await:',
                        //   path,
                        //   'Extracted filename:',
                        //   filename
                        // );
                    }
                    catch (error) {
                        console.error('Error waiting for panel context or getting path:', error);
                        filename = ''; // Set filename to empty on error
                    }
                }
                else {
                    // If panel is null (e.g., last notebook closed), clear filename
                    // console.debug('Signal received with null panel. Clearing filename.');
                    filename = ''; // Explicitly set to empty
                }
                // Check if the derived filename is different from the current state
                if (filename !== currentNotebookFileName) {
                    // console.debug(
                    //   'updateFilename: Notebook changed (',
                    //   currentNotebookFileName,
                    //   '->',
                    //   filename,
                    //   '). Clearing cell contexts...'
                    // );
                    // Clear cell contexts first
                    setActiveContexts(currentContexts => currentContexts.filter(ctx => ctx.type !== 'notebook-cell'));
                    // Then, update the filename state
                    setCurrentNotebookFileName(filename);
                }
                else {
                    // If the filename is the same, just log (no state updates needed)
                    // console.debug(
                    //   'updateFilename: Filename (',
                    //   filename,
                    //   ') is the same as current state. No updates needed.'
                    // );
                }
                // console.debug('updateFilename complete.');
            };
            // --- Attempt to set initial filename (Best Effort) ---
            const initialPanel = tracker.currentWidget;
            if (initialPanel) {
                // Use the async handler for the initial panel too, for consistency
                // console.debug(
                //   'Initial check: Found active widget. Calling updateFilename...'
                // );
                updateFilename(tracker, initialPanel);
            }
            else {
                // console.debug(
                //   'Initial check: No active widget found. Waiting for signal.'
                // );
            }
            // --- Connect the signal ---
            tracker.currentChanged.connect(updateFilename);
            // console.debug('Connected to tracker.currentChanged');
            // --- Cleanup ---
            return () => {
                // console.debug('Disconnecting from tracker.currentChanged');
                // Clear timeout (if we were still using it)
                // if (timeoutId) clearTimeout(timeoutId);
                // Disconnect signal
                if (notebookController === null || notebookController === void 0 ? void 0 : notebookController._notebookTracker) {
                    try {
                        notebookController._notebookTracker.currentChanged.disconnect(updateFilename);
                    }
                    catch (error) {
                        console.warn('Error disconnecting from tracker signal:', error);
                    }
                }
            };
        }
        else {
            // Handle case where controller or tracker is not available
            console.debug('Notebook controller or tracker not found initially.');
            setCurrentNotebookFileName(''); // Reset filename if controller/tracker disappears
        }
        // Dependency array: Re-run the effect if notebookController instance changes
        // No longer need currentNotebookFileName here as we read from signal/initial check
    }, [notebookController]);
    // --- Callback functions using the controller logic ---
    const addCurrentNotebookContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        setActiveContexts(currentContexts => controller.addCurrentNotebookContext(currentContexts));
    }, [controller]);
    const addContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((contextToAdd) => {
        setActiveContexts(currentContexts => controller.addContext(currentContexts, contextToAdd));
    }, [controller]); // Depends only on the stable controller instance
    const addCurrentCellContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        setActiveContexts(currentContexts => controller.addCurrentCellContext(currentContexts));
    }, [controller]);
    const removeContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((contextToRemove) => {
        setActiveContexts(currentContexts => controller.removeContext(currentContexts, contextToRemove));
    }, [controller]);
    // Read functions need access to current state or controller
    const hasCurrentCellInContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        // Logic is in controller, pass current state
        return controller.hasCurrentCellInContext(activeContexts);
    }, [controller, activeContexts]); // Depends on controller and current state
    const getContextNameCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((context) => {
        // Logic is in controller, doesn't need activeContexts state here
        return controller.getContextName(context);
    }, [controller]);
    const getContextDataForApiCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        // Logic is in controller, pass current state
        return controller.getContextDataForApi(activeContexts, currentNotebookInContext);
    }, [controller, activeContexts, currentNotebookInContext]);
    const setCurrentNotebookInContextCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((value) => {
        setCurrentNotebookInContext(value);
    }, []);
    // --- Effect to handle external command for adding cell context ---
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const handleAddCellContextEvent = () => {
            console.debug('Received jovyanai:addCurrentCellContext event, calling callback.');
            addCurrentCellContextCallback();
        };
        document.body.addEventListener('jovyanai:addCurrentCellContext', handleAddCellContextEvent);
        console.debug('ChatContextProvider mounted, listening for jovyanai:addCurrentCellContext event.');
        return () => {
            document.body.removeEventListener('jovyanai:addCurrentCellContext', handleAddCellContextEvent);
            console.debug('ChatContextProvider unmounted, removing listener for jovyanai:addCurrentCellContext event.');
        };
    }, [addCurrentCellContextCallback]); // Re-run if the callback instance changes
    // --- Context Value ---
    // Assemble the value to be provided by the context
    const providerValue = (0,react__WEBPACK_IMPORTED_MODULE_0__.useMemo)(() => ({
        activeContexts,
        currentNotebookInContext,
        currentNotebookFileName,
        addContext: addContextCallback,
        addCurrentCellContext: addCurrentCellContextCallback,
        hasCurrentCellInContext: hasCurrentCellInContextCallback,
        removeContext: removeContextCallback,
        getContextName: getContextNameCallback,
        getContextDataForApi: getContextDataForApiCallback,
        addCurrentNotebookContext: addCurrentNotebookContextCallback,
        setCurrentNotebookInContext: setCurrentNotebookInContextCallback
    }), [
        activeContexts,
        currentNotebookInContext,
        currentNotebookFileName,
        addContextCallback,
        addCurrentCellContextCallback,
        hasCurrentCellInContextCallback,
        removeContextCallback,
        getContextNameCallback,
        getContextDataForApiCallback,
        addCurrentNotebookContextCallback,
        setCurrentNotebookInContextCallback
    ]);
    return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ChatContext.Provider, { value: providerValue }, children);
};
// --- Hook to use the context ---
const useChatContext = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(ChatContext);
    if (!context) {
        throw new Error('useChatContext must be used within a ChatContextProvider');
    }
    return context;
};


/***/ }),

/***/ "./lib/chatAssistant/chatContextController.js":
/*!****************************************************!*\
  !*** ./lib/chatAssistant/chatContextController.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatContextController: () => (/* binding */ ChatContextController)
/* harmony export */ });
/* harmony import */ var _types_context__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./types/context */ "./lib/chatAssistant/types/context.js");

// --- Controller Class (Logic) ---
// Export the class so it can be imported by the provider
class ChatContextController {
    constructor(notebookController) {
        this.notebookController = notebookController;
    }
    // Modifier logic: Takes current state, returns new state
    addContext(currentContexts, contextToAdd) {
        if (!currentContexts.some(existingCtx => existingCtx.id === contextToAdd.id)) {
            return [...currentContexts, contextToAdd];
        }
        return currentContexts; // Return unchanged state if already exists
    }
    // Modifier logic: Takes current state, returns new state
    addCurrentCellContext(currentContexts) {
        const notebookPath = this.notebookController.getCurrentNotebookFilePath();
        const activeCell = this.notebookController.activeCell;
        if (activeCell) {
            const cellContext = new _types_context__WEBPACK_IMPORTED_MODULE_0__.NotebookCellContext(activeCell.model.id, notebookPath);
            if (!currentContexts.some(ctx => ctx.id === cellContext.id && ctx.type === 'notebook-cell')) {
                console.debug('Controller adding current cell context', cellContext.id);
                return [...currentContexts, cellContext];
            }
            else {
                console.debug('Controller: Current cell context already exists', cellContext.id);
            }
        }
        else {
            console.warn('Controller: No active cell found to add context for.');
        }
        return currentContexts; // Return unchanged state if no cell or already exists
    }
    addCurrentNotebookContext(currentContexts) {
        const notebookPath = this.notebookController.getCurrentNotebookFilePath();
        if (notebookPath) {
            const notebookContext = new _types_context__WEBPACK_IMPORTED_MODULE_0__.NotebookContext(notebookPath);
            return this.addContext(currentContexts, notebookContext);
        }
        return currentContexts;
    }
    // Modifier logic: Takes current state, returns new state
    removeContext(currentContexts, contextToRemove) {
        return currentContexts.filter(ctx => ctx.id !== contextToRemove.id);
    }
    // Read logic: Operates on current state
    hasCurrentCellInContext(currentContexts) {
        var _a;
        const activeCellId = (_a = this.notebookController.activeCell) === null || _a === void 0 ? void 0 : _a.model.id;
        if (!activeCellId) {
            return false;
        }
        return currentContexts.some(ctx => ctx.id === activeCellId && ctx.type === 'notebook-cell');
    }
    // Read logic: Doesn't depend on activeContexts state, only notebookController
    getContextName(context) {
        // Ensure notebookController is available, handle potential undefined case
        return this.notebookController
            ? context.getDisplayName(this.notebookController)
            : 'Context';
    }
    // Read logic: Operates on current state
    getContextDataForApi(currentContexts, currentNotebookInContext) {
        if (!this.notebookController) {
            console.error('NotebookController not available in ChatContextController logic');
            return { currentNotebook: [], selectedCells: [] };
        }
        const currentNotebookContext = new _types_context__WEBPACK_IMPORTED_MODULE_0__.NotebookContext(this.notebookController.getCurrentNotebookFilePath());
        const currentNotebook = currentNotebookInContext
            ? currentNotebookContext.getContextDataForApi(this.notebookController)
            : [];
        const selectedCells = currentContexts
            .filter(ctx => ctx.type === 'notebook-cell')
            .map(ctx => ctx.getContextDataForApi(this.notebookController));
        return {
            currentNotebook: currentNotebook,
            selectedCells: selectedCells.filter((cell) => cell !== null)
        };
    }
}


/***/ }),

/***/ "./lib/chatAssistant/components/chat-header.js":
/*!*****************************************************!*\
  !*** ./lib/chatAssistant/components/chat-header.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatHeader: () => (/* binding */ ChatHeader)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_chat_header_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/chat-header.css */ "./style/chat-header.css");
/* harmony import */ var _context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../context/NotebookControllerContext */ "./lib/context/NotebookControllerContext.js");
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../jovyanClient */ "./lib/jovyanClient.js");
/* harmony import */ var _utils_time__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../utils/time */ "./lib/utils/time.js");

// import { RefreshCw, X } from 'lucide-react'; // Removed unused imports


 // Added jovyanClient import
 // Added time utility import
const ChatHeader = ({ title, onNewChat, onLoadChat }) => {
    const notebookController = (0,_context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_2__.useNotebookController)();
    const [showHistory, setShowHistory] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [recentChats, setRecentChats] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const historyDropdownRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null); // Ref for dropdown
    const handleClose = () => {
        notebookController.runCommand('jovyanai:toggle-chat');
    };
    const handleHistoryClick = async () => {
        if (showHistory) {
            setShowHistory(false);
        }
        else {
            try {
                if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_3__.clientIsConnected)()) {
                    console.debug('Client not connected, skipping getChats');
                    setRecentChats([]);
                    setShowHistory(true);
                    return;
                }
                const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_3__.getJovyanClient)();
                const chats = await client.getChats();
                // Sort by creation date descending and take the top 10
                const sortedChats = chats
                    .sort((a, b) => new Date(b.created_at).getTime() -
                    new Date(a.created_at).getTime())
                    .slice(0, 10);
                setRecentChats(sortedChats);
                setShowHistory(true);
            }
            catch (error) {
                console.error('Failed to fetch chat history:', error);
                // Handle error appropriately, maybe show a notification
            }
        }
    };
    const handleHistoryItemClick = (chatId) => {
        onLoadChat(chatId);
        setShowHistory(false); // Close dropdown after selection
    };
    // Close dropdown if clicked outside
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const handleClickOutside = (event) => {
            if (historyDropdownRef.current &&
                !historyDropdownRef.current.contains(event.target)) {
                setShowHistory(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [historyDropdownRef]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-header" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h2", null, title),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "header-controls" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "header-button add-button", onClick: onNewChat, title: "New Chat" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "+")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "history-container", ref: historyDropdownRef },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "header-button history-button", onClick: handleHistoryClick, title: "Chat History" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "\u21BB")),
                showHistory && recentChats.length > 0 && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "history-dropdown" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", null, recentChats.map(chat => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", { key: chat.id, onClick: () => handleHistoryItemClick(chat.id) },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "chat-title" }, chat.title || 'Untitled Chat'),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "chat-time" }, (0,_utils_time__WEBPACK_IMPORTED_MODULE_4__.formatRelativeTime)(chat.created_at)))))))),
                showHistory && recentChats.length === 0 && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "history-dropdown" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "No chat history found.")))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "header-button close-button", onClick: handleClose, title: "Close Chat" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "\u00D7")))));
};


/***/ }),

/***/ "./lib/chatAssistant/components/chat-input.js":
/*!****************************************************!*\
  !*** ./lib/chatAssistant/components/chat-input.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatInput: () => (/* binding */ ChatInput)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_menu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./context-menu */ "./lib/chatAssistant/components/context-menu.js");
/* harmony import */ var _style_chat_input_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/chat-input.css */ "./style/chat-input.css");
/* harmony import */ var _ChatContextProvider__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../ChatContextProvider */ "./lib/chatAssistant/ChatContextProvider.js");
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../jovyanClient */ "./lib/jovyanClient.js");
/* harmony import */ var _utils_authDialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../utils/authDialog */ "./lib/utils/authDialog.js");
/* harmony import */ var _context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../context/NotebookControllerContext */ "./lib/context/NotebookControllerContext.js");
'use client';








const ChatInput = ({ onSendMessage, onCancel, disabled = false }) => {
    const [message, setMessage] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const textareaRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const chatContext = (0,_ChatContextProvider__WEBPACK_IMPORTED_MODULE_2__.useChatContext)();
    const notebookController = (0,_context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_3__.useNotebookController)();
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim() || disabled) {
            return;
        }
        if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_4__.clientIsConnected)()) {
            console.debug('Chat submit: Jovyan client not connected. Prompting for auth.');
            const userCancelled = await (0,_utils_authDialog__WEBPACK_IMPORTED_MODULE_5__.showAuthReminderDialog)(notebookController === null || notebookController === void 0 ? void 0 : notebookController.settingRegistry);
            if (userCancelled) {
                console.debug('Chat submit: Auth dialog cancelled by user.');
                return;
            }
            if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_4__.clientIsConnected)()) {
                console.warn("Chat submit: Auth dialog closed but client still not connected.");
                return;
            }
        }
        const userMessage = {
            role: 'user',
            content: message.trim(),
            contexts: chatContext.activeContexts
        };
        await onSendMessage(userMessage);
        setMessage('');
        if (textareaRef.current) {
            textareaRef.current.style.height = '24px';
        }
    };
    const handleTextareaChange = (e) => {
        setMessage(e.target.value);
        const textarea = e.target;
        textarea.style.height = '24px';
        const newHeight = Math.min(textarea.scrollHeight, 200);
        textarea.style.height = `${newHeight}px`;
    };
    const handleKeyDown = (e) => {
        // Submit on Enter without Shift
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (message.trim() && !disabled) {
                handleSubmit(e);
            }
        }
        // Cancel on Shift + Cmd/Ctrl + Backspace when disabled
        if (e.shiftKey && (e.metaKey || e.ctrlKey) && e.key === 'Backspace') {
            if (disabled) {
                e.preventDefault(); // Prevent default backspace behavior
                onCancel(); // Call the cancel function
            }
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-input-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: handleSubmit, className: "chat-form" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_menu__WEBPACK_IMPORTED_MODULE_6__.ContextMenu, { disabled: disabled }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "input-wrapper" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("textarea", { ref: textareaRef, className: "chat-textarea", value: message, onChange: handleTextareaChange, onKeyDown: handleKeyDown, placeholder: "Ask, learn, brainstorm", disabled: disabled })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "input-controls" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "send-container" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "model-name" }, "gemini-2.5-pro"),
                    disabled ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "chat-input-cancel-button", onClick: onCancel }, "Cancel Run")) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit", className: "send-button", disabled: !message.trim() },
                        "Send ",
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "enter-icon" }, "\u21B5"))))))));
};


/***/ }),

/***/ "./lib/chatAssistant/components/chat-interface.js":
/*!********************************************************!*\
  !*** ./lib/chatAssistant/components/chat-interface.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatInterface: () => (/* binding */ ChatInterface)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_chat_interface_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/chat-interface.css */ "./style/chat-interface.css");
/* harmony import */ var _chat_header__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./chat-header */ "./lib/chatAssistant/components/chat-header.js");
/* harmony import */ var _chat_input__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./chat-input */ "./lib/chatAssistant/components/chat-input.js");
/* harmony import */ var _chat_message__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./chat-message */ "./lib/chatAssistant/components/chat-message.js");
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../jovyanClient */ "./lib/jovyanClient.js");
/* harmony import */ var _ChatContextProvider__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../ChatContextProvider */ "./lib/chatAssistant/ChatContextProvider.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utils */ "./lib/chatAssistant/components/utils.js");
'use client';









const getLastChat = async () => {
    if (!(0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.clientIsConnected)()) {
        console.debug('Client not connected, skipping getLastChat');
        return null;
    }
    const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.getJovyanClient)();
    const chats = await client.getChats();
    // console.debug('Get chats', chats);
    // if last chat exists
    if (chats.length > 0) {
        const lastChat = chats.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())[0];
        // if last chat has messages
        const messages = await client.getMessages(lastChat.id);
        // console.debug('Get messages', messages);
        if (messages.length > 0) {
            return { chat: lastChat, messages: messages };
        }
    }
};
const ChatInterface = () => {
    const [messages, setMessages] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [currentChatId, setCurrentChatId] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    // const [toolUses, setToolUses] = useState<IToolUse[]>([]);
    // const [currentTool, setCurrentTool] = useState<IToolUse | null>(null);
    const [isStreaming, setIsStreaming] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [isThinking, setIsThinking] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const messagesEndRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const chatContextController = (0,_ChatContextProvider__WEBPACK_IMPORTED_MODULE_3__.useChatContext)();
    const [chatTitle, setChatTitle] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    // Function to handle creating a new chat
    const handleNewChat = () => {
        setMessages([]); // Reset the messages state
        setCurrentChatId(null);
        setIsStreaming(false);
        setIsThinking(false);
        setChatTitle('New Chat');
        // only create new chat on the first message sent
    };
    const handleCancel = async () => {
        console.debug('Cancel requested');
        // TODO: Implement actual cancellation logic with the JovyanClient
        setIsStreaming(false);
        setIsThinking(false);
        // Optionally remove the streaming placeholder message
        setMessages(prev => prev.filter(msg => !(msg.role === 'assistant' && msg.isStreaming === true)));
    };
    // at mount, get latest chat
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const loadLatestChat = async () => {
            const lastChat = await getLastChat();
            if (!lastChat) {
                console.debug('No last chat found, skipping loadLatestChat');
                setChatTitle('New Chat');
                return;
            }
            console.debug('Get latest chat', lastChat);
            if (lastChat) {
                // console.debug('Loading latest chat', lastChat);
                setCurrentChatId(lastChat.chat.id);
                const sortedMessages = lastChat.messages
                    .sort((a, b) => new Date(a.created_at).getTime() -
                    new Date(b.created_at).getTime())
                    .map(msg => ({
                    role: msg.sender,
                    content: msg.content
                }));
                setMessages(sortedMessages);
                setChatTitle(lastChat.chat.title ||
                    (0,_utils__WEBPACK_IMPORTED_MODULE_4__.getChatTitle)(lastChat.messages[0].content));
                //scroll to bottom
                const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.getJovyanClient)();
                client.setCurrentChatId(lastChat.chat.id);
                // Scrolling is now handled by the useEffect hook below
            }
        };
        loadLatestChat();
        padChatColumn('off');
        // Scrolling on initial load is handled within loadLatestChat
    }, []);
    const handleSendMessage = async (message) => {
        // start streaming response
        setIsStreaming(true);
        // add user message to messages
        setMessages(prev => [...prev, message]);
        setIsThinking(true);
        setIsStreaming(false);
        padChatColumn('on'); // Add padding before scrolling
        const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.getJovyanClient)();
        await client.connect();
        if (!currentChatId) {
            console.debug('Creating new chat');
            // get title from first 3 words of user message with first word capitalized
            const title = message.content
                .split(' ')
                .slice(0, 3)
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
            const newChat = await client.createChat(title);
            setChatTitle(title);
            setCurrentChatId(newChat.id);
            client.setCurrentChatId(newChat.id); // Ensure new chat ID is set
        }
        console.debug('Current chat ID', currentChatId);
        const contextData = chatContextController.getContextDataForApi();
        console.debug('Context data', contextData);
        // --- End Context Gathering Logic ---
        let accumulatedContent = '';
        let firstChunkReceived = false;
        client
            .sendChatUserMessageStream(message.content, contextData, chunk => {
            if (!firstChunkReceived) {
                setIsThinking(false);
                setIsStreaming(true);
                firstChunkReceived = true;
                const initialNewMessage = {
                    role: 'assistant',
                    content: chunk,
                    isStreaming: true
                };
                setMessages(prev => [...prev, initialNewMessage]);
                accumulatedContent = chunk;
            }
            else {
                accumulatedContent += chunk;
                setMessages(prev => {
                    const updatedMessages = [...prev];
                    const streamingMessageIndex = updatedMessages.findIndex(msg => msg.role === 'assistant' && msg.isStreaming === true);
                    if (streamingMessageIndex !== -1) {
                        updatedMessages[streamingMessageIndex].content = accumulatedContent;
                    }
                    return updatedMessages;
                });
            }
        })
            .then(async () => {
            setMessages(prev => {
                return prev.map(msg => msg.role === 'assistant' && msg.isStreaming === true
                    ? { ...msg, content: accumulatedContent, isStreaming: false }
                    : msg);
            });
            setIsStreaming(false);
        })
            .catch(error => {
            console.error('Error streaming chat message:', error);
            setIsThinking(false);
            setIsStreaming(false);
            setMessages(prev => prev.filter(msg => !(msg.role === 'assistant' && msg.isStreaming === true)));
        })
            .finally(() => {
            setIsThinking(false);
            setIsStreaming(false);
            padChatColumn('off');
        });
    };
    const padChatColumn = (status) => {
        var _a;
        const chatColumn = (_a = messagesEndRef.current) === null || _a === void 0 ? void 0 : _a.parentElement;
        if (!chatColumn) {
            return;
        }
        if (status === 'on') {
            // Use a large padding value to ensure enough scroll space
            chatColumn.style.paddingBottom = '100vh';
        }
        else {
            // Reset padding, calculating dynamically based on the last user message if possible
            const defaultPadding = '80px';
            chatColumn.style.paddingBottom = defaultPadding; // Set default first
            // Try to calculate padding based on the last user message height
            // -1: messagesEndRef, -2: last assistant message, -3: last user message
            const lastUserMessageBox = chatColumn.children[chatColumn.children.length - 3];
            if (lastUserMessageBox && lastUserMessageBox.clientHeight) {
                // Calculate required padding to keep the user message visible, with some buffer
                // Aim to have roughly (viewport height - message height - buffer) space below the message
                const calculatedPadding = `calc(100vh - ${lastUserMessageBox.offsetTop}px - ${lastUserMessageBox.clientHeight}px - 100px)`; // Adjust 100px buffer as needed
                // Use the larger of the default or calculated padding
                chatColumn.style.paddingBottom = `max(${defaultPadding}, ${calculatedPadding})`;
                console.debug('Calculated paddingBottom:', chatColumn.style.paddingBottom);
            }
            else {
                console.debug('Could not find last user message box or its height for padding calculation.');
            }
        }
    };
    // Auto-scroll user message to top when they send one
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        // Only scroll if there are messages and the last one is from user
        if (messages.length > 0 && messages[messages.length - 1].role === 'user') {
            scrollMessages();
        }
        else {
            // For other cases (initial load, history load, assistant message finished), scroll to bottom
            // Ensure messages exist before trying to scroll
            if (messages.length > 0 && isStreaming === false) {
                padChatColumn('off');
                requestAnimationFrame(() => {
                    var _a;
                    (_a = messagesEndRef.current) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ behavior: 'smooth' });
                });
            }
        }
    }, [messages.length]); // Dependency ensures this runs when messages array updates
    // Function to scroll the latest message (usually user's) towards the top
    const scrollMessages = () => {
        // Use requestAnimationFrame to ensure DOM updates are painted
        requestAnimationFrame(() => {
            if (messagesEndRef.current) {
                const parentElement = messagesEndRef.current.parentElement;
                console.debug('Scroll messages', parentElement);
                if (!parentElement) {
                    return;
                }
                // Target the second to last element, which should be the user's latest message
                const lastMessageBox = messagesEndRef.current.previousElementSibling;
                console.debug('Scroll messages', lastMessageBox);
                if (!lastMessageBox) {
                    // If no message yet, scroll to top
                    parentElement.scrollTo({ top: 0, behavior: 'smooth' });
                    return;
                }
                // Calculate the desired scroll position to bring the message near the top
                const messageTop = lastMessageBox.offsetTop;
                const desiredScrollTop = messageTop - 100; // Adjust the offset (100px) as needed
                console.debug('Scroll messages', desiredScrollTop);
                parentElement.scrollTo({
                    top: desiredScrollTop,
                    behavior: 'smooth'
                });
            }
        });
    };
    // Render messages and tool uses in chronological order
    const renderChatItems = () => {
        // Combine messages and tool uses and sort by timestamp
        const allItems = [
            ...messages.map(msg => ({
                type: 'message',
                data: msg
            }))
        ];
        return allItems.map((item, index) => {
            if (item.type === 'message') {
                return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_message__WEBPACK_IMPORTED_MODULE_5__.ChatMessage, { key: index, message: item.data });
            }
            // Handle other item types if necessary
            return null;
        });
    };
    const handleLoadChat = async (chatId) => {
        console.debug('Loading chat', chatId);
        const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.getJovyanClient)();
        client.setCurrentChatId(chatId);
        const fetchedMessages = await client.getMessages(chatId);
        const sortedMessages = fetchedMessages
            .sort((a, b) => new Date(a.created_at).getTime() -
            new Date(b.created_at).getTime())
            .map(msg => ({
            role: msg.sender,
            content: msg.content
        }));
        setMessages(sortedMessages);
        setCurrentChatId(chatId);
        // Scroll to bottom after messages are set and rendered
        // Scrolling is now handled by the useEffect hook below
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_header__WEBPACK_IMPORTED_MODULE_6__.ChatHeader, { title: chatTitle, onNewChat: handleNewChat, onLoadChat: handleLoadChat }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "chat-content" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "messages-container" },
                renderChatItems(),
                isThinking && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_message__WEBPACK_IMPORTED_MODULE_5__.ChatMessage, { message: { role: 'assistant', content: '' }, isThinking: true })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: messagesEndRef }))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_input__WEBPACK_IMPORTED_MODULE_7__.ChatInput, { onSendMessage: handleSendMessage, onCancel: handleCancel, disabled: isStreaming || isThinking })));
};


/***/ }),

/***/ "./lib/chatAssistant/components/chat-message.js":
/*!******************************************************!*\
  !*** ./lib/chatAssistant/components/chat-message.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatMessage: () => (/* binding */ ChatMessage)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _code_block__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./code-block */ "./lib/chatAssistant/components/code-block.js");
/* harmony import */ var _inline_code__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./inline-code */ "./lib/chatAssistant/components/inline-code.js");
/* harmony import */ var _style_chat_message_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../style/chat-message.css */ "./style/chat-message.css");
/* harmony import */ var _ChatContextProvider__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../ChatContextProvider */ "./lib/chatAssistant/ChatContextProvider.js");
/* harmony import */ var react_markdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-markdown */ "webpack/sharing/consume/default/react-markdown/react-markdown");
/* harmony import */ var react_markdown__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_markdown__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var remark_gfm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! remark-gfm */ "webpack/sharing/consume/default/remark-gfm/remark-gfm");
/* harmony import */ var remark_gfm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(remark_gfm__WEBPACK_IMPORTED_MODULE_3__);
'use client';

 // Now we will use this again
 // Import the new component



 // Restore GFM
const ChatMessage = ({ message, isThinking // Destructure the new prop
 }) => {
    const chatContextController = (0,_ChatContextProvider__WEBPACK_IMPORTED_MODULE_4__.useChatContext)();
    // Render content using ReactMarkdown with custom component for code blocks
    const renderMarkdownContent = (content) => {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react_markdown__WEBPACK_IMPORTED_MODULE_2___default()), { remarkPlugins: [(remark_gfm__WEBPACK_IMPORTED_MODULE_3___default())], components: {
                // Only override `code`. Differentiate based on className presence.
                code({ node, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    if (match) {
                        // ClassName like "language-python" exists - render Block
                        const codeContent = String(children).replace(/\n$/, '');
                        const language = match[1];
                        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_code_block__WEBPACK_IMPORTED_MODULE_5__.CodeBlock, { code: codeContent, language: language });
                    }
                    else {
                        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_inline_code__WEBPACK_IMPORTED_MODULE_6__.InlineCode, { ...props }, children);
                    }
                }
                // No `pre` override needed anymore
            } }, content));
    };
    // If isThinking is true, render a simple indicator
    if (isThinking) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `message assistant thinking` },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "message-content" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "thinking-indicator" },
                    "Thinking",
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "dot" }, "."),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "dot" }, "."),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "dot" }, ".")))));
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `message ${message.role}` },
        message.role === 'user' &&
            message.contexts &&
            message.contexts.length > 0 && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "message-header" }, message.contexts.map((context, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { key: index, className: `context-tag ${context.type}` },
            "@",
            chatContextController.getContextName(context)))))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "message-content" }, renderMarkdownContent(message.content))));
};


/***/ }),

/***/ "./lib/chatAssistant/components/code-block.js":
/*!****************************************************!*\
  !*** ./lib/chatAssistant/components/code-block.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CodeBlock: () => (/* binding */ CodeBlock)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lucide-react */ "webpack/sharing/consume/default/lucide-react/lucide-react");
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(lucide_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @codemirror/view */ "webpack/sharing/consume/default/@codemirror/view");
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_codemirror_view__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _codemirror_lang_python__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @codemirror/lang-python */ "./node_modules/@codemirror/lang-python/dist/index.js");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_code_block_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../style/code-block.css */ "./style/code-block.css");
/* harmony import */ var _context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../context/NotebookControllerContext */ "./lib/context/NotebookControllerContext.js");
'use client';








const CodeBlock = ({ code, language }) => {
    const [isCopied, setIsCopied] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const editorRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const viewRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)();
    const notebookController = (0,_context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_6__.useNotebookController)();
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (editorRef.current) {
            if (viewRef.current) {
                viewRef.current.destroy();
            }
            const extensions = [
                _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__.jupyterTheme,
                _codemirror_view__WEBPACK_IMPORTED_MODULE_2__.EditorView.editable.of(false),
                _codemirror_state__WEBPACK_IMPORTED_MODULE_3__.EditorState.readOnly.of(true),
                _codemirror_view__WEBPACK_IMPORTED_MODULE_2__.EditorView.lineWrapping
            ];
            if (language === 'python') {
                extensions.push((0,_codemirror_lang_python__WEBPACK_IMPORTED_MODULE_7__.python)());
            }
            const state = _codemirror_state__WEBPACK_IMPORTED_MODULE_3__.EditorState.create({
                doc: code,
                extensions
            });
            const view = new _codemirror_view__WEBPACK_IMPORTED_MODULE_2__.EditorView({
                state: state,
                parent: editorRef.current
            });
            viewRef.current = view;
            return () => {
                view.destroy();
                viewRef.current = undefined;
            };
        }
    }, [code, language]);
    const handleCopy = () => {
        navigator.clipboard.writeText(code).then(() => {
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 2000);
        });
    };
    const handleApplyCode = () => {
        const cell = notebookController.currentCell;
        if (cell) {
            notebookController.writeCodeInCell(cell, code);
            // Optionally run the cell after applying
            // notebookController.runCell(cell);
        }
    };
    const handleInsertCodeBelow = () => {
        const currentCellIndex = notebookController.currentCellIndex;
        notebookController.insertCell(currentCellIndex + 1, code);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "code-block" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "code-header" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "language-tag" }, language),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "code-header-buttons" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: handleCopy, className: "code-action-button", title: "Copy code" }, isCopied ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Check, { size: 14 }) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Clipboard, { size: 14 })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: handleApplyCode, className: "code-action-button", title: "Apply to active cell" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Play, { size: 14 })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: handleInsertCodeBelow, className: "code-action-button", title: "Insert cell below" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Plus, { size: 14 })))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "code-content", ref: editorRef })));
};


/***/ }),

/***/ "./lib/chatAssistant/components/context-badge.js":
/*!*******************************************************!*\
  !*** ./lib/chatAssistant/components/context-badge.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ContextBadge: () => (/* binding */ ContextBadge)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _style_context_badge_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../style/context-badge.css */ "./style/context-badge.css");
'use client';

// import { X } from 'lucide-react'; // Removed unused import
 // Import icons

const ContextBadge = ({ contextName, contextType, onRemove }) => {
    // Revert display logic to original
    // const displayName = contextType === 'notebook' ? 'Notebook' : 'Cell';
    // const badgeClass = `context-badge ${contextType}`;
    // Determine the icon based on contextType
    const Icon = contextType === 'notebook' || contextType === 'current-notebook-context'
        ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.notebookIcon
        : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.codeIcon;
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `context-badge ${contextType}` },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "context-badge-prefix" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Icon.react, { tag: "span", className: "context-badge-icon" })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "context-badge-name" }, contextName),
        contextType !== 'current-notebook-context' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "context-badge-remove", onClick: e => {
                e.stopPropagation();
                onRemove();
            } }, "\u00D7"))));
};


/***/ }),

/***/ "./lib/chatAssistant/components/context-menu.js":
/*!******************************************************!*\
  !*** ./lib/chatAssistant/components/context-menu.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ContextMenu: () => (/* binding */ ContextMenu)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _context_badge__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./context-badge */ "./lib/chatAssistant/components/context-badge.js");
/* harmony import */ var _ChatContextProvider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../ChatContextProvider */ "./lib/chatAssistant/ChatContextProvider.js");
'use client';



const ContextMenu = ({ disabled = false }) => {
    const [showContextMenu, setShowContextMenu] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const contextMenuRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const contextButtonRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const chatContextController = (0,_ChatContextProvider__WEBPACK_IMPORTED_MODULE_1__.useChatContext)();
    // Toggle context menu
    const toggleContextMenu = (e) => {
        e.stopPropagation();
        setShowContextMenu(!showContextMenu);
    };
    // Close context menu when clicking outside
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const handleClickOutside = (event) => {
            if (contextMenuRef.current &&
                !contextMenuRef.current.contains(event.target) &&
                contextButtonRef.current &&
                !contextButtonRef.current.contains(event.target)) {
                setShowContextMenu(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);
    // const handleAddNotebookContext = () => {
    //   chatContextController.addCurrentNotebookContext();
    //   setShowContextMenu(false);
    // };
    const handleAddCellContext = () => {
        try {
            chatContextController.addCurrentCellContext();
        }
        catch (error) {
            console.error('Error creating cell context:', error);
        }
        setShowContextMenu(false);
    };
    // Determine active states
    const isNotebookContextActive = chatContextController.currentNotebookInContext;
    const isCellContextActive = chatContextController.hasCurrentCellInContext();
    const onRemoveContext = (context) => {
        chatContextController.removeContext(context);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "context-badges" },
        ' ',
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "add-context-button", onClick: toggleContextMenu, ref: contextButtonRef, disabled: disabled }, "@"),
        showContextMenu && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "context-menu", ref: contextMenuRef },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `context-menu-item ${isCellContextActive ? 'disabled' : ''}`, onClick: isCellContextActive ? undefined : handleAddCellContext, style: {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, "This Cell"),
                isCellContextActive && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { marginLeft: '10px' } }, "\u2713"))))),
        isNotebookContextActive && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_badge__WEBPACK_IMPORTED_MODULE_2__.ContextBadge, { key: 'current-notebook-context', contextName: chatContextController.currentNotebookFileName, contextType: 'current-notebook-context', onRemove: () => { } })),
        chatContextController.activeContexts.map(context => {
            // Use a more robust key, displayName might not be unique enough long term
            const key = `${context.type}-${chatContextController.getContextName(context)}`;
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_badge__WEBPACK_IMPORTED_MODULE_2__.ContextBadge, { key: key, contextName: chatContextController.getContextName(context), contextType: context.type, onRemove: () => onRemoveContext(context) }));
        })));
};


/***/ }),

/***/ "./lib/chatAssistant/components/inline-code.js":
/*!*****************************************************!*\
  !*** ./lib/chatAssistant/components/inline-code.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InlineCode: () => (/* binding */ InlineCode)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! lucide-react */ "webpack/sharing/consume/default/lucide-react/lucide-react");
/* harmony import */ var lucide_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(lucide_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _style_inline_code_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../style/inline-code.css */ "./style/inline-code.css");
'use client';


 // We will create this file next
const InlineCode = ({ children }) => {
    const [isCopied, setIsCopied] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const codeString = react__WEBPACK_IMPORTED_MODULE_0___default().Children.toArray(children).join(''); // Extract text content
    const handleCopy = (event) => {
        event.stopPropagation(); // Prevent potential parent handlers
        navigator.clipboard.writeText(codeString).then(() => {
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 1500); // Reset after 1.5 seconds
        });
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", { className: "inline-code-container" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "inline-code-text" }, children),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: handleCopy, className: "inline-code-copy-button", title: "Copy code" }, isCopied ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Check, { size: 12 }) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(lucide_react__WEBPACK_IMPORTED_MODULE_1__.Clipboard, { size: 12 }))));
};


/***/ }),

/***/ "./lib/chatAssistant/components/utils.js":
/*!***********************************************!*\
  !*** ./lib/chatAssistant/components/utils.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getChatTitle: () => (/* binding */ getChatTitle)
/* harmony export */ });
const getChatTitle = (message) => {
    // get title from first 3 words of user message with first word capitalized
    return message
        .split(' ')
        .slice(0, 3)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};


/***/ }),

/***/ "./lib/chatAssistant/index.js":
/*!************************************!*\
  !*** ./lib/chatAssistant/index.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   attachChatAssistant: () => (/* binding */ attachChatAssistant)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_chat_interface__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/chat-interface */ "./lib/chatAssistant/components/chat-interface.js");
/* harmony import */ var _style_chatAssistant_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../style/chatAssistant.css */ "./style/chatAssistant.css");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _style_icons_logo_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../style/icons/logo.svg */ "./style/icons/logo.svg");
/* harmony import */ var _context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../context/NotebookControllerContext */ "./lib/context/NotebookControllerContext.js");
/* harmony import */ var _ChatContextProvider__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./ChatContextProvider */ "./lib/chatAssistant/ChatContextProvider.js");










function attachChatAssistant(options) {
    const { app, notebookController } = options;
    // Initialize the chat assistant
    const content = document.createElement('div');
    content.id = 'jupyterlab-chat-extension-root';
    content.className = 'jupyterlab-chat-extension';
    // Create a JupyterLab widget
    const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget({ node: content });
    widget.id = 'jupyterlab-chat-assistant-widget';
    const chatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.LabIcon({
        name: 'jovyan::chat',
        svgstr: _style_icons_logo_svg__WEBPACK_IMPORTED_MODULE_6__
    });
    widget.title.icon = chatIcon;
    widget.title.caption = 'Jovyan AI Chat Assistant';
    widget.title.closable = true;
    widget.title.className = 'jp-mod-opacity-50';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.WidgetTracker({
        namespace: 'jupyterlab-chat-extension'
    });
    tracker.add(widget);
    // Add the widget to the right area
    app.shell.add(widget, 'right', { activate: false });
    // Initialize React component
    const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_3__.createRoot)(content);
    // Wrap ChatInterface with the Provider
    root.render(react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_context_NotebookControllerContext__WEBPACK_IMPORTED_MODULE_7__.NotebookControllerContext.Provider, { value: notebookController }, react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ChatContextProvider__WEBPACK_IMPORTED_MODULE_8__.ChatContextProvider, {
        children: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_chat_interface__WEBPACK_IMPORTED_MODULE_9__.ChatInterface)
    })));
    // Register the command to activate and focus
    app.commands.addCommand('jovyanai:toggle-chat', {
        label: 'Toggle Chat Assistant',
        execute: () => {
            const labShell = app.shell;
            const sidePanel = Array.from(labShell.widgets('right')).find(widget => widget.id === 'jupyterlab-chat-assistant-widget');
            const wasExpanded = (sidePanel === null || sidePanel === void 0 ? void 0 : sidePanel.isVisible) || false;
            const inputElement = widget.node.querySelector('#chat-input');
            if (wasExpanded) {
                labShell.collapseRight();
            }
            else {
                labShell.activateById(widget.id);
                requestAnimationFrame(() => {
                    if (inputElement) {
                        inputElement.focus();
                    }
                    else {
                        console.warn('Chat input element (#chat-input) not found for focusing after activation.');
                    }
                });
            }
            return null;
        }
    });
    // Add keyboard shortcut
    app.commands.addKeyBinding({
        command: 'jovyanai:toggle-chat',
        keys: ['Alt B'],
        selector: 'body'
    });
    // Register the command to add the current cell to context
    app.commands.addCommand('jovyanai:addCurrentCellContext', {
        label: 'Add Current Cell to Chat Context',
        execute: () => {
            const activeCell = notebookController.currentCell; // Use currentCell property
            if (activeCell) {
                // Check if the chat widget is visible, open if not
                if (!widget.isVisible) {
                    console.debug('Chat panel not visible. Activating chat panel.');
                    app.shell.activateById(widget.id);
                }
                console.debug('Dispatching jovyanai:addCurrentCellContext event for cell:', activeCell.model.id);
                const event = new CustomEvent('jovyanai:addCurrentCellContext');
                document.body.dispatchEvent(event);
            }
            else {
                console.warn('No active cell found to add to context.');
            }
            return null;
        }
    });
    // Add keyboard shortcut for adding cell context
    app.commands.addKeyBinding({
        command: 'jovyanai:addCurrentCellContext',
        keys: ['Alt L'],
        selector: 'body'
    });
}


/***/ }),

/***/ "./lib/chatAssistant/types/context.js":
/*!********************************************!*\
  !*** ./lib/chatAssistant/types/context.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookCellContext: () => (/* binding */ NotebookCellContext),
/* harmony export */   NotebookContext: () => (/* binding */ NotebookContext)
/* harmony export */ });
/* harmony import */ var _utils_extractCellData__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../utils/extractCellData */ "./lib/utils/extractCellData.js");

class NotebookCellContext {
    constructor(cellId, notebookId) {
        this.type = 'notebook-cell';
        this.id = cellId;
        this.notebookId = notebookId;
    }
    getDisplayName(notebookController) {
        const cell = notebookController.getCellById(this.id);
        if (cell) {
            const index = notebookController.getCurrentNotebookCells().indexOf(cell);
            return `cell ${index >= 0 ? index + 1 : '?'.toString()}`;
        }
        return 'Unknown Cell';
    }
    getContextDataForApi(notebookController) {
        const cell = notebookController.getCellById(this.id);
        if (cell) {
            return (0,_utils_extractCellData__WEBPACK_IMPORTED_MODULE_0__.convertCellToCellData)(cell);
        }
        return null;
    }
}
class NotebookContext {
    constructor(notebookId) {
        this.type = 'notebook';
        this.id = notebookId;
    }
    getDisplayName(notebookController) {
        // return the filename of the notebook
        return this.id.split('/').pop() || this.id;
    }
    getContextDataForApi(notebookController) {
        const cells = notebookController.getCurrentNotebookCells();
        return cells.map(cell => (0,_utils_extractCellData__WEBPACK_IMPORTED_MODULE_0__.convertCellToCellData)(cell));
    }
}


/***/ }),

/***/ "./lib/context/NotebookControllerContext.js":
/*!**************************************************!*\
  !*** ./lib/context/NotebookControllerContext.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookControllerContext: () => (/* binding */ NotebookControllerContext),
/* harmony export */   useNotebookController: () => (/* binding */ useNotebookController)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const NotebookControllerContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
const useNotebookController = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(NotebookControllerContext);
    if (context === undefined) {
        throw new Error('useNotebookController must be used within a NotebookControllerProvider');
    }
    return context;
};


/***/ }),

/***/ "./lib/controller.js":
/*!***************************!*\
  !*** ./lib/controller.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NotebookController: () => (/* binding */ NotebookController)
/* harmony export */ });
class NotebookController {
    constructor(notebookTracker, commands, settingRegistry) {
        this._notebookTracker = notebookTracker;
        this._commands = commands;
        this._settingRegistry = settingRegistry;
    }
    get settingRegistry() {
        return this._settingRegistry;
    }
    get activeCell() {
        var _a;
        return (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
    }
    addElementAfterCellInput(cell, element) {
        const cellNode = cell.node;
        // Append the parentContainer to the input area of the cell
        const inputArea = cellNode.querySelector('.jp-Cell-inputWrapper');
        if (inputArea) {
            inputArea.insertAdjacentElement('afterend', element);
        }
        else {
            cellNode.appendChild(element);
        }
    }
    addElementInCellChild(cell, element) {
        const cellNode = cell.node;
        cellNode.appendChild(element);
    }
    writeCodeInCell(cell, code) {
        cell.model.sharedModel.setSource(code);
    }
    runCell(cell) {
        const notebook = this._notebookTracker.currentWidget;
        if (notebook) {
            notebook.content.activeCellIndex = notebook.content.widgets.indexOf(cell);
            this._commands.execute('notebook:run-cell');
        }
    }
    insertCell(index, content) {
        var _a;
        const notebook = this._notebookTracker.currentWidget;
        if (notebook) {
            (_a = notebook.model) === null || _a === void 0 ? void 0 : _a.sharedModel.insertCell(index, {
                cell_type: 'code',
                source: content
            });
        }
    }
    get currentCell() {
        var _a;
        return (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
    }
    get currentCellIndex() {
        var _a;
        return ((_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCellIndex) || 0;
    }
    getPreviousCells(cell) {
        var _a;
        const notebook = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        const index = notebook === null || notebook === void 0 ? void 0 : notebook.activeCellIndex;
        if (index !== undefined && notebook) {
            return notebook.widgets.slice(0, index);
        }
        return [];
    }
    getNextCells(cell) {
        var _a;
        const notebook = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        const index = this.currentCellIndex;
        if (index !== undefined && notebook) {
            return notebook.widgets.slice(index + 1);
        }
        return [];
    }
    getLanguage() {
        var _a;
        const notebook = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model;
        const language = (notebook === null || notebook === void 0 ? void 0 : notebook.defaultKernelLanguage) || 'python';
        return language;
    }
    runCommand(command) {
        this._commands.execute(command);
    }
    getCurrentNotebookCells() {
        var _a;
        const notebook = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (notebook) {
            return notebook.widgets.map(widget => widget);
        }
        return [];
    }
    getCurrentNotebookFileName() {
        var _a, _b;
        // Get path from the widget's context contentsModel
        const path = (_b = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.context.contentsModel) === null || _b === void 0 ? void 0 : _b.path;
        if (path) {
            // Extract filename from the path
            const parts = path.split('/');
            return parts[parts.length - 1];
        }
        return '';
    }
    getCurrentNotebookFilePath() {
        var _a, _b;
        // Get path from the widget's context contentsModel
        const path = (_b = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.context.contentsModel) === null || _b === void 0 ? void 0 : _b.path;
        return path || '';
    }
    getCellById(id) {
        var _a;
        const notebook = (_a = this._notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (notebook) {
            return notebook.widgets.find(widget => widget.model.id === id);
        }
        return null;
    }
    getNotebookByPath(path) {
        let notebook = null;
        this._notebookTracker.forEach(panel => {
            if (panel.context.path === path) {
                notebook = panel;
            }
        });
        return notebook;
    }
}


/***/ }),

/***/ "./lib/handleCodeGeneration.js":
/*!*************************************!*\
  !*** ./lib/handleCodeGeneration.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   setupCodeGenerationStream: () => (/* binding */ setupCodeGenerationStream)
/* harmony export */ });
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./jovyanClient */ "./lib/jovyanClient.js");

const _convertCellToCellData = (cell) => {
    const outputs = [];
    if (cell.model.type === 'code') {
        const codeCell = cell.model;
        const outputArea = codeCell.outputs;
        for (let i = 0; i < outputArea.length; i++) {
            const output = outputArea.get(i);
            if (output) {
                const outputData = output.toJSON();
                switch (outputData.output_type) {
                    case 'execute_result': {
                        const execOutput = {
                            output_type: 'execute_result',
                            data: outputData.data
                        };
                        outputs.push(execOutput);
                        break;
                    }
                    case 'stream': {
                        const streamOutput = {
                            output_type: 'stream',
                            name: String(outputData.name || 'stdout'),
                            text: Array.isArray(outputData.text)
                                ? outputData.text.map(String)
                                : [String(outputData.text || '')]
                        };
                        outputs.push(streamOutput);
                        break;
                    }
                    case 'display_data': {
                        const displayOutput = {
                            output_type: 'display_data',
                            data: outputData.data
                        };
                        outputs.push(displayOutput);
                        break;
                    }
                    case 'error': {
                        const errorOutput = {
                            output_type: 'error',
                            ename: String(outputData.ename || 'Error'),
                            evalue: String(outputData.evalue || 'Unknown error'),
                            traceback: Array.isArray(outputData.traceback)
                                ? outputData.traceback.map(String)
                                : []
                        };
                        outputs.push(errorOutput);
                        break;
                    }
                }
            }
        }
    }
    return {
        cell_type: cell.model.type,
        source: cell.model.sharedModel.source,
        outputs: outputs
    };
};
const setupCodeGenerationStream = async (options) => {
    const client = await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_0__.getJovyanClient)();
    // We'll store tokens here as they come in.
    let done = false;
    const chunks = [];
    client
        .generateCodeStream({
        currentCell: _convertCellToCellData(options.currentCell),
        previousCells: options.previousCells.map(_convertCellToCellData),
        nextCells: options.nextCells.map(_convertCellToCellData),
        prompt: options.userInput,
        language: options.language,
        stream: true
    }, chunk => {
        chunks.push(chunk);
    })
        .then(() => {
        // Resolve the promise when the stream is finished
        done = true;
    })
        .catch(error => {
        // Handle errors here
        console.error('Error generating code stream:', error);
        throw error;
    });
    return (async function* () {
        while (!done || chunks.length > 0) {
            if (chunks.length > 0) {
                const nextToken = chunks.shift();
                if (nextToken) {
                    yield nextToken;
                }
            }
            else {
                await new Promise(resolve => setTimeout(resolve, 50));
            }
        }
    })();
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _cellOps_jovyanCellController__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./cellOps/jovyanCellController */ "./lib/cellOps/jovyanCellController.js");
/* harmony import */ var _controller__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./controller */ "./lib/controller.js");
/* harmony import */ var _jovyanClient__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./jovyanClient */ "./lib/jovyanClient.js");
/* harmony import */ var _chatAssistant__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./chatAssistant */ "./lib/chatAssistant/index.js");






/**
 * Initialization data for the @jovyanai/labextension extension.
 */
const plugin = {
    id: '@jovyanai/labextension:plugin',
    description: 'A JupyterLab extension to integrate Jovyan AI',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: async (app, notebookTracker, settingRegistry) => {
        console.debug('JupyterLab extension @jovyanai/labextension is activated! Hello!');
        // Initialize settings if settingRegistry is available
        if (settingRegistry) {
            await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.initializeClient)(settingRegistry);
            // Listen for setting changes
            settingRegistry
                .load('@jovyanai/labextension:plugin')
                .then(settings => {
                settings.changed.connect(async () => {
                    await (0,_jovyanClient__WEBPACK_IMPORTED_MODULE_2__.initializeClient)(settingRegistry);
                });
            })
                .catch(error => {
                console.error('Failed to load settings for @jovyanai/labextension:', error);
            });
        }
        // Only proceed if settingRegistry is available
        if (settingRegistry) {
            const notebookController = new _controller__WEBPACK_IMPORTED_MODULE_3__.NotebookController(notebookTracker, app.commands, settingRegistry);
            // on notebook active cell changed, add the cell activate button
            notebookTracker.activeCellChanged.connect((sender, cell) => {
                if (cell) {
                    const jovyanCellController = new _cellOps_jovyanCellController__WEBPACK_IMPORTED_MODULE_4__.JovyanCellController(cell, notebookController);
                    jovyanCellController.activate();
                }
            });
            // When a cell is executed, add the fix error button
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect((sender, args) => {
                const cell = args.cell;
                console.debug('Cell executed', cell);
                if (cell) {
                    const jovyanCellController = new _cellOps_jovyanCellController__WEBPACK_IMPORTED_MODULE_4__.JovyanCellController(cell, notebookController);
                    jovyanCellController.addFixErrorButton();
                }
            });
            // Initialize and attach the chat assistant
            (0,_chatAssistant__WEBPACK_IMPORTED_MODULE_5__.attachChatAssistant)({ app, notebookController });
        }
        else {
            console.warn('ISettingRegistry not found, Jovyan AI features disabled.');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/jovyanClient.js":
/*!*****************************!*\
  !*** ./lib/jovyanClient.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   clientIsConnected: () => (/* binding */ clientIsConnected),
/* harmony export */   getJovyanClient: () => (/* binding */ getJovyanClient),
/* harmony export */   initializeClient: () => (/* binding */ initializeClient)
/* harmony export */ });
/* harmony import */ var _jovyan_client__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jovyan/client */ "webpack/sharing/consume/default/@jovyan/client/@jovyan/client");
/* harmony import */ var _jovyan_client__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jovyan_client__WEBPACK_IMPORTED_MODULE_0__);

// Default settings
let backendUrl = 'wss://backend.jovyan-ai.com';
let authToken = '';
// Global client instance
let jovyanClientInstance = null;
// Connection state management
let isConnecting = false;
let connectionPromise = null;
// Function to initialize settings from the registry
const initializeClient = async (settingRegistry) => {
    console.debug('Initializing client from settings...');
    try {
        const settings = await settingRegistry.load('@jovyanai/labextension:plugin');
        backendUrl = settings.get('backendUrl').composite;
        authToken = settings.get('authToken').composite;
        console.debug(`Loaded settings: backendUrl=${backendUrl}, authToken=${authToken ? '***' : '<empty>'}`);
        // No explicit disconnect needed; creating a new instance will let the old one be garbage collected.
        // Create the new client instance but DO NOT connect yet.
        console.debug('Creating new JovyanClient instance.');
        jovyanClientInstance = new _jovyan_client__WEBPACK_IMPORTED_MODULE_0__.JovyanClient(backendUrl, authToken, '');
        // Reset connection state as we have a new instance
        isConnecting = false;
        connectionPromise = null;
        console.debug('JovyanClient instance created (not connected yet).');
    }
    catch (error) {
        console.error('Failed to load settings or create client instance:', error);
        // Keep the old instance if creation failed? Or set to null? Setting to null seems safer.
        jovyanClientInstance = null;
        isConnecting = false;
        connectionPromise = null;
    }
};
const getJovyanClient = async () => {
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
            }
            else {
                console.warn('getJovyanClient: Waited for connection, but it failed.');
                // Decide whether to retry or throw. Throwing seems safer to avoid loops.
                throw new Error('Connection attempt failed.');
            }
        }
        catch (error) {
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
        }
        catch (error) {
            console.error('getJovyanClient: Failed to connect/start session:', error);
            connectionPromise = null; // Clear promise on failure
            throw error; // Propagate the error
        }
        finally {
            // Regardless of success or failure, we are no longer in the 'connecting' state
            isConnecting = false;
            console.debug('getJovyanClient: Connection attempt finished.');
            // We don't clear connectionPromise here, it resolves or rejects
        }
    })();
    try {
        await connectionPromise;
        return currentInstance;
    }
    catch (error) {
        // The error is already logged in the promise handler
        // Rethrow to signal failure to the caller of getJovyanClient
        throw error;
    }
};
const clientIsConnected = () => {
    var _a;
    // Use optional chaining in case instance is null
    return (_a = jovyanClientInstance === null || jovyanClientInstance === void 0 ? void 0 : jovyanClientInstance.isConnected) !== null && _a !== void 0 ? _a : false;
};


/***/ }),

/***/ "./lib/utils/authDialog.js":
/*!*********************************!*\
  !*** ./lib/utils/authDialog.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   showAuthReminderDialog: () => (/* binding */ showAuthReminderDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _authReminder_authReminder__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../authReminder/authReminder */ "./lib/authReminder/authReminder.js");




 // Adjust path as needed
/**
 * Shows an authentication reminder dialog.
 * @param settingRegistry - The ISettingRegistry instance.
 * @returns A promise that resolves to true if the dialog was cancelled by the user,
 *          false otherwise (e.g., connection established or dialog closed implicitly).
 */
function showAuthReminderDialog(settingRegistry) {
    // Returns a promise that resolves to true if cancelled, false otherwise.
    return new Promise(resolve => {
        if (!settingRegistry) {
            console.error('SettingRegistry not provided to showAuthReminderDialog.');
            resolve(true); // Treat as cancellation if registry is missing
            return;
        }
        const body = document.createElement('div');
        const root = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_2__.createRoot)(body);
        let dialog = null;
        let bodyWidget = null;
        let explicitlyClosed = false;
        const closeDialogAndResolve = (didCancel) => {
            if (explicitlyClosed) {
                return;
            }
            explicitlyClosed = true;
            console.debug(`Auth Dialog close requested. Cancelled: ${didCancel}`);
            try {
                root.unmount();
            }
            catch (e) {
                console.warn('Error unmounting React root during close:', e);
            }
            if (dialog && !dialog.isDisposed) {
                dialog.dispose();
                dialog = null;
            }
            if (bodyWidget && !bodyWidget.isDisposed) {
                bodyWidget.dispose();
                bodyWidget = null;
            }
            resolve(didCancel);
        };
        const handleConnected = () => {
            console.debug('AuthReminder reported connected.');
            closeDialogAndResolve(false);
        };
        const handleCancel = () => {
            console.debug('AuthReminder cancelled by component.');
            closeDialogAndResolve(true);
        };
        const authReminderComponent = react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_authReminder_authReminder__WEBPACK_IMPORTED_MODULE_4__.AuthReminder, {
            settingRegistry: settingRegistry,
            onConnected: handleConnected,
            onCancel: handleCancel
        });
        root.render(authReminderComponent);
        bodyWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: body });
        dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
            title: 'Jovyan AI Authentication',
            body: bodyWidget,
            buttons: []
        });
        dialog.disposed.connect(() => {
            dialog = null;
            if (bodyWidget && !bodyWidget.isDisposed) {
                bodyWidget.dispose();
            }
            bodyWidget = null;
        });
        if (bodyWidget) {
            bodyWidget.disposed.connect(() => {
                bodyWidget = null;
            });
        }
        dialog
            .launch()
            .then(() => {
            console.debug('Dialog launch() promise resolved (dialog closed).');
            if (!explicitlyClosed) {
                console.debug('Dialog closed implicitly. Treating as Cancel.');
                closeDialogAndResolve(true);
            }
            dialog = null;
            bodyWidget = null;
        })
            .catch(error => {
            if (!explicitlyClosed) {
                console.error('Error during dialog lifecycle:', error);
                console.debug('Treating dialog error as Cancel.');
                closeDialogAndResolve(true);
            }
            else {
                console.debug('Dialog launch promise rejected, likely due to explicit closure:', error);
            }
            dialog = null;
            bodyWidget = null;
        });
    });
}


/***/ }),

/***/ "./lib/utils/extractCellData.js":
/*!**************************************!*\
  !*** ./lib/utils/extractCellData.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   convertCellToCellData: () => (/* binding */ convertCellToCellData)
/* harmony export */ });
const convertCellToCellData = (cell) => {
    const outputs = [];
    if (cell.model.type === 'code') {
        const codeCell = cell.model;
        const outputArea = codeCell.outputs;
        for (let i = 0; i < outputArea.length; i++) {
            const output = outputArea.get(i);
            if (output) {
                const outputData = output.toJSON();
                switch (outputData.output_type) {
                    case 'execute_result': {
                        const execOutput = {
                            output_type: 'execute_result',
                            data: outputData.data
                        };
                        outputs.push(execOutput);
                        break;
                    }
                    case 'stream': {
                        const streamOutput = {
                            output_type: 'stream',
                            name: String(outputData.name || 'stdout'),
                            text: Array.isArray(outputData.text)
                                ? outputData.text.map(String)
                                : [String(outputData.text || '')]
                        };
                        outputs.push(streamOutput);
                        break;
                    }
                    case 'display_data': {
                        const displayOutput = {
                            output_type: 'display_data',
                            data: outputData.data
                        };
                        outputs.push(displayOutput);
                        break;
                    }
                    case 'error': {
                        const errorOutput = {
                            output_type: 'error',
                            ename: String(outputData.ename || 'Error'),
                            evalue: String(outputData.evalue || 'Unknown error'),
                            traceback: Array.isArray(outputData.traceback)
                                ? outputData.traceback.map(String)
                                : []
                        };
                        outputs.push(errorOutput);
                        break;
                    }
                }
            }
        }
    }
    return {
        cell_type: cell.model.type,
        source: cell.model.sharedModel.source,
        outputs: outputs
    };
};


/***/ }),

/***/ "./lib/utils/time.js":
/*!***************************!*\
  !*** ./lib/utils/time.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   formatRelativeTime: () => (/* binding */ formatRelativeTime)
/* harmony export */ });
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.round((now.getTime() - date.getTime()) / 1000);
    const minutes = Math.round(seconds / 60);
    const hours = Math.round(minutes / 60);
    const days = Math.round(hours / 24);
    const weeks = Math.round(days / 7);
    const months = Math.round(days / 30); // Approximate
    const years = Math.round(days / 365); // Approximate
    if (seconds < 60) {
        return `${seconds}s ago`;
    }
    if (minutes < 60) {
        return `${minutes}m ago`;
    }
    if (hours < 24) {
        return `${hours}h ago`;
    }
    if (days < 7) {
        return `${days}d ago`;
    }
    if (weeks < 4) {
        return `${weeks}w ago`;
    } // Up to 4 weeks
    if (months < 12) {
        return `${months}mo ago`;
    }
    return `${years}y ago`;
}


/***/ }),

/***/ "./style/chat-header.css":
/*!*******************************!*\
  !*** ./style/chat-header.css ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_chat_header_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./chat-header.css */ "./node_modules/css-loader/dist/cjs.js!./style/chat-header.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_chat_header_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_chat_header_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_chat_header_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_chat_header_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/chat-input.css":
/*!******************************!*\
  !*** ./style/chat-input.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_chat_input_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./chat-input.css */ "./node_modules/css-loader/dist/cjs.js!./style/chat-input.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_chat_input_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_chat_input_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_chat_input_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_chat_input_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/chat-interface.css":
/*!**********************************!*\
  !*** ./style/chat-interface.css ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_chat_interface_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./chat-interface.css */ "./node_modules/css-loader/dist/cjs.js!./style/chat-interface.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_chat_interface_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_chat_interface_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_chat_interface_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_chat_interface_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/chat-message.css":
/*!********************************!*\
  !*** ./style/chat-message.css ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_chat_message_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./chat-message.css */ "./node_modules/css-loader/dist/cjs.js!./style/chat-message.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_chat_message_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_chat_message_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_chat_message_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_chat_message_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/chatAssistant.css":
/*!*********************************!*\
  !*** ./style/chatAssistant.css ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_chatAssistant_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./chatAssistant.css */ "./node_modules/css-loader/dist/cjs.js!./style/chatAssistant.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_chatAssistant_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_chatAssistant_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_chatAssistant_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_chatAssistant_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/code-block.css":
/*!******************************!*\
  !*** ./style/code-block.css ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_code_block_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./code-block.css */ "./node_modules/css-loader/dist/cjs.js!./style/code-block.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_code_block_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_code_block_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_code_block_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_code_block_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/context-badge.css":
/*!*********************************!*\
  !*** ./style/context-badge.css ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_context_badge_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./context-badge.css */ "./node_modules/css-loader/dist/cjs.js!./style/context-badge.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_context_badge_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_context_badge_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_context_badge_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_context_badge_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/icons/logo.svg":
/*!******************************!*\
  !*** ./style/icons/logo.svg ***!
  \******************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" standalone=\"no\"?>\n<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 20010904//EN\"\n \"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd\">\n<svg version=\"1.0\" xmlns=\"http://www.w3.org/2000/svg\"\n width=\"512.000000pt\" height=\"512.000000pt\" viewBox=\"0 0 512.000000 512.000000\"\n preserveAspectRatio=\"xMidYMid meet\">\n\n<g transform=\"translate(0.000000,512.000000) scale(0.100000,-0.100000)\"\nfill=\"#000000\" stroke=\"none\">\n<path d=\"M0 2560 l0 -2560 2560 0 2560 0 0 2560 0 2560 -2560 0 -2560 0 0\n-2560z m3595 1212 c47 -24 96 -73 120 -122 26 -50 29 -173 5 -226 -68 -157\n-287 -205 -416 -91 -107 93 -123 250 -39 362 74 96 225 131 330 77z m-516\n-149 c-10 -38 -19 -68 -19 -69 0 -1 -46 -4 -102 -7 -314 -19 -725 -201 -1033\n-459 -440 -367 -641 -812 -493 -1091 84 -156 259 -225 543 -214 190 8 372 48\n537 119 40 17 49 26 58 57 29 102 34 189 35 546 0 336 -2 373 -18 402 -20 38\n-70 66 -149 83 l-58 13 0 92 0 92 38 7 c20 3 163 6 318 6 209 0 285 -3 297\n-13 16 -11 17 -48 15 -490 -2 -262 1 -477 5 -477 5 0 82 73 171 163 172 172\n247 271 312 412 50 108 78 224 72 300 l-5 61 58 32 58 32 10 -37 c45 -161 -38\n-428 -206 -663 -81 -112 -259 -295 -399 -409 l-101 -82 -7 -53 c-16 -143 -96\n-342 -181 -454 -91 -120 -232 -210 -400 -252 -77 -20 -305 -41 -375 -35 -19 2\n-50 4 -67 4 l-33 1 0 119 0 120 48 5 c189 22 278 56 367 138 55 52 106 118 89\n118 -4 0 -48 -13 -98 -29 -146 -46 -271 -64 -446 -64 -178 0 -263 18 -389 79\n-175 86 -281 265 -281 475 0 260 162 572 439 849 378 377 911 631 1338 639\nl72 1 -20 -67z\"/>\n</g>\n</svg>\n";

/***/ }),

/***/ "./style/inline-code.css":
/*!*******************************!*\
  !*** ./style/inline-code.css ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_inline_code_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./inline-code.css */ "./node_modules/css-loader/dist/cjs.js!./style/inline-code.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_inline_code_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_inline_code_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_inline_code_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_inline_code_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lezer_common-webpack_sharing_consume_default_react-dom.71a39fecd4b9d6fd1a26.js.map