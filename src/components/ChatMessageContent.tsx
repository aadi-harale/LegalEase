import React from 'react';
import { RedactedText } from './RedactedText';

interface ChatMessageContentProps {
  text: string;
  onCitationClick: (quote: string) => void;
}

export const ChatMessageContent: React.FC<ChatMessageContentProps> = ({ text, onCitationClick }) => {
  // Regex to match [Citation: "exact quote"]
  const citationRegex = /\[Citation:\s*"([^"]+)"\]/g;
  
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match;

  while ((match = citationRegex.exec(text)) !== null) {
    // Push preceding text
    if (match.index > lastIndex) {
      parts.push(
        <RedactedText key={`text-${lastIndex}`} text={text.substring(lastIndex, match.index)} />
      );
    }
    
    // Push the citation badge
    const quote = match[1];
    parts.push(
      <button
        key={`citation-${match.index}`}
        onClick={() => onCitationClick(quote)}
        className="inline-flex items-center mx-1 px-2 py-0.5 rounded-md bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 text-xs font-semibold hover:bg-blue-200 dark:hover:bg-blue-800/40 transition-colors border border-blue-200 dark:border-blue-800/50 cursor-pointer group"
        title="View source context"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-1 opacity-70 group-hover:opacity-100">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        Source
      </button>
    );

    lastIndex = citationRegex.lastIndex;
  }

  // Push remaining text
  if (lastIndex < text.length) {
    parts.push(
      <RedactedText key={`text-${lastIndex}`} text={text.substring(lastIndex)} />
    );
  }

  return <>{parts}</>;
};
