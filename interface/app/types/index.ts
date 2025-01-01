export type FileWithStatus = {
	file: File;
	status?:
		| "waiting"
		| "uploading"
		| "uploaded"
		| "error"
		| "canceled"
		| "gotPSU"
		| null;
	isRetrying?: boolean;
	controller: AbortController;
	insuranceSide?: "front" | "back";
};
