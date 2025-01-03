import { create } from "zustand";

type ProcessStatus =
	| "idle"
	| "extracting"
	| "standardizing"
	| "completed"
	| "error";

interface TextProcessingStore {
	status: ProcessStatus;
	error: string | null;
	extractedText: string;
	standardizedText: string;
	setStatus: (status: ProcessStatus) => void;
	setError: (error: string | null) => void;
	setExtractedText: (text: string) => void;
	setStandardizedText: (text: string) => void;
	reset: () => void;
}

export const useTextProcessing = create<TextProcessingStore>((set) => ({
	status: "idle",
	error: null,
	extractedText: "",
	standardizedText: "",
	setStatus: (status) => set({ status }),
	setError: (error) => set({ error }),
	setExtractedText: (text) => set({ extractedText: text }),
	setStandardizedText: (text) => set({ standardizedText: text }),
	reset: () =>
		set({
			status: "idle",
			error: null,
			extractedText: "",
			standardizedText: "",
		}),
}));
