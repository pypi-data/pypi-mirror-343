export const getChatTitle = (message: string) => {
  // get title from first 3 words of user message with first word capitalized
  return message
    .split(' ')
    .slice(0, 3)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
