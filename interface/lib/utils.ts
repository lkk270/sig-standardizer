import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function formatFileSize(bytes: bigint) {
	const KB = BigInt(1000);
	const MB = BigInt(1000000);
	const GB = BigInt(1000000000);
	const TB = BigInt(1000000000000);

	if (bytes < KB) return bytes + " Bytes";
	else if (bytes < MB) return (Number(bytes) / Number(KB)).toFixed(1) + " KB";
	else if (bytes < GB) return (Number(bytes) / Number(MB)).toFixed(1) + " MB";
	else if (bytes < TB) return (Number(bytes) / Number(GB)).toFixed(2) + " GB";
	return (Number(bytes) / Number(TB)).toFixed(2) + " TB";
}
