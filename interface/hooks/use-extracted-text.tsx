import { create } from "zustand";

interface ExtractedTextStore {
	extractedText: string;
	setExtractedText: (text: string) => void;
}

export const useExtractedText = create<ExtractedTextStore>((set) => ({
	extractedText: "",
	setExtractedText: (text) => set({ extractedText: text }),
}));
