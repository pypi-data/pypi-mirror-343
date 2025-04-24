/// <reference types="react" />
interface CopyToClipboardProps {
    text?: string;
    targetRef?: React.RefObject<HTMLElement>;
    className?: string;
    contentType?: string;
    description?: string;
}
declare const CopyToClipboard: React.FC<CopyToClipboardProps>;
export default CopyToClipboard;
