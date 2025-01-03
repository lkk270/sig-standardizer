"use client";

import React, { useRef, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import { Inbox } from "lucide-react";
import { FileWithStatus } from "@/app/types";
import { useTextProcessing } from "@/hooks/use-text-processing";
import { cn } from "@/lib/utils";

// Define the props expected by the Dropzone component
interface DropzoneProps {
	onChangeSingleFile?: (file: FileWithStatus | null) => void;
	className?: string;
}

// Create the Dropzone component receiving props
export function Dropzone({
	onChangeSingleFile,
	className,
	...props
}: DropzoneProps) {
	const { status } = useTextProcessing();
	const isProcessing = status === "extracting" || status === "standardizing";

	// Initialize state variables using the useState hook
	const fileInputRef = useRef<HTMLInputElement | null>(null);
	const [isOverArea, setIsOverArea] = useState(false);
	const title = "Click or drag a JPEG/JPG or PNG to this area to upload";

	// Function to handle drag over event
	const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		e.stopPropagation();
		setIsOverArea(true);
	};

	const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		e.stopPropagation();
		setIsOverArea(false);
	};

	// Function to handle drop event
	const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
		if (isProcessing) {
			toast.warning("Must wait for processing to finish");
			return;
		}
		e.preventDefault();
		e.stopPropagation();
		const { files } = e.dataTransfer;
		handleFiles(files);
		setIsOverArea(false);
	};

	// Function to handle file input change event
	const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { files } = e.target;
		if (files) {
			handleFiles(files);
			e.target.value = "";
		}
	};

	// Function to handle processing of uploaded files
	const handleFiles = (files: FileList) => {
		const maxSize = 10485760;
		const maxSizeError = "10 Mb";
		const newFiles: FileWithStatus[] = []; // Define as array of FileWithStatus
		for (let i = 0; i < files.length; i++) {
			if (files[i].size > maxSize) {
				// Optionally, alert the user that the file is too large
				toast.error(
					`${files[i].name} is too large. Maximum file size is ${maxSizeError}.`
				);
				continue; // Skip this file and continue with the next one
			}
			const file = files[i];
			// Convert each File into a FileWithStatus object
			newFiles.push({ file: file, controller: new AbortController() });
		}

		if (onChangeSingleFile) {
			const file = newFiles[0];
			if (
				!!file &&
				file.file.type !== "image/png" &&
				file.file.type !== "image/jpeg"
			) {
				toast.error("Invalid file type. Must be a PNG or JPEG file!", {
					duration: 3000,
				});
				return;
			}
			if (!!file) {
				onChangeSingleFile(file);
			}
		}
	};

	const handleButtonClick = () => {
		if (isProcessing) {
			toast.warning("Must wait for processing to finish");
			return;
		}
		if (fileInputRef.current) {
			fileInputRef.current.click();
		}
	};

	return (
		<>
			<Card
				onClick={handleButtonClick}
				className={cn(
					"border-2 border-dashed bg-muted hover:cursor-pointer hover:border-muted-foreground/50",
					isOverArea && "border-muted-foreground/50",
					className
				)}
				{...props}
			>
				<CardContent
					className="flex flex-col items-center justify-center space-y-2 px-2 py-4 text-xs"
					onDragOver={handleDragOver}
					onDragLeave={handleDragLeave}
					onDrop={handleDrop}
				>
					<div className="flex flex-col items-center justify-center text-muted-foreground">
						<Inbox color={"#4f5eff"} className="w-8 h-8 mb-2" />
						<span className="font-medium text-sm">{title}</span>
						<input
							ref={fileInputRef}
							type="file"
							accept={`image/png, image/jpeg`}
							onChange={handleFileInputChange}
							className="hidden"
							multiple={false}
						/>
					</div>
				</CardContent>
			</Card>
		</>
	);
}
