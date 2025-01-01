"use client";

import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
} from "@/components/ui/card";
import { useState } from "react";
import { Trash, RefreshCw, XCircle } from "lucide-react";
import { Dropzone } from "@/components/file-upload/dropzone";
import { FileWithStatus } from "@/app/types";
import { Spinner } from "@/components/reusable/spinner";
import { cn, formatFileSize } from "@/lib/utils";
import { Separator } from "@/components/ui/separator";
import { useIsLoading } from "@/hooks/use-is-loading";
import { Button } from "@/components/ui/button";

interface UploadFilesFormProps {
	requestRecordsCode?: {
		id: string;
		userId: string;
		createdAt: Date;
		parentFolderId: string;
		hasUploaded: boolean;
		token: string;
		expires: Date;
		isValid: boolean;
		providerEmail: string;
	};
}

export const FileUploadForm = ({
	requestRecordsCode,
}: UploadFilesFormProps) => {
	const [calledSetHasUploadToTrue, setCalledSetHasUploadToTrue] = useState(
		requestRecordsCode?.hasUploaded
	);
	const [file, setFile] = useState<FileWithStatus | null>(null);
	const { isLoading, setIsLoading } = useIsLoading();

	const updateFileStatus = (
		status: "uploaded" | "error" | "canceled" | "uploading" | "gotPSU"
	) => {
		if (file) {
			setFile((prev) => (prev ? { ...prev, status, isRetrying: false } : null));
		}
	};

	const handleUpload = async (isForRetry = false) => {
		if (isLoading || !file) return;

		if (file.status === "canceled") {
			file.controller = new AbortController();
		}
		setIsLoading(true);

		try {
			updateFileStatus("uploading");

			let body = {
				fileName: file.file.name,
				contentType: file.file.type,
				size: file.file.size,
				accessToken: requestRecordsCode?.token,
			};

			const response = await fetch(
				!!requestRecordsCode ? "/api/rr-file-upload" : "/api/tpa-file-upload",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify(body),
					signal: file.controller.signal,
				}
			);

			updateFileStatus("gotPSU");
			const { url, fields, fileIdResponse, parentFolderNameResponse } =
				await response.json();

			const formData = new FormData();
			Object.entries(fields).forEach(([key, value]) => {
				formData.append(key, value as string);
			});
			formData.append("file", file.file as any);

			const uploadResponse = await fetch(url, {
				method: "POST",
				body: formData,
			});

			if (!uploadResponse.ok) throw new Error(`File upload to storage failed.`);

			updateFileStatus("uploaded");
		} catch (error: any) {
			if (
				error.toString().includes("signal is aborted") ||
				error.toString().includes("The user aborted a request")
			) {
				updateFileStatus("canceled");
			} else {
				updateFileStatus("error");
			}
		}

		setIsLoading(false);
	};

	const handleRemoveFile = () => {
		setFile(null);
	};

	const cancelUpload = () => {
		if (file) {
			file.controller.abort();
		}
	};

	return (
		<Card className="flex flex-col h-72 max-w-full w-full border border-primary/10 rounded-xl overflow-hidden">
			<div
				className={cn(
					"w-full grid",
					requestRecordsCode && calledSetHasUploadToTrue
						? "grid-cols-2"
						: "grid-cols-1"
				)}
			></div>
			<div className="flex justify-center w-full">
				<CardContent className="flex flex-col flex-grow justify-center max-w-[800px] w-full">
					<CardHeader>
						<Dropzone
							onChangeSingleFile={(newFile) => setFile(newFile)}
							className="w-full"
						/>
					</CardHeader>

					<div className="overflow-y-scroll max-h-[45vh] gap-y-2 flex flex-col">
						{file && (
							<div className="px-4">
								<div className="flex items-center text-muted-foreground overflow-hidden">
									{(file.status === "uploading" ||
										file.status === "gotPSU") && (
										<div className="flex-shrink-0 pr-2">
											<Spinner size="default" loaderType="loader2" />
										</div>
									)}
									{(file.status === "error" || file.status === "canceled") && (
										<div
											title="retry"
											role="button"
											className="flex-shrink-0 pr-2"
											onClick={() => handleUpload(true)}
										>
											<RefreshCw className="w-4 h-4 text-[#4f5eff]" />
										</div>
									)}
									<div
										className={cn(
											"text-sm flex flex-grow min-w-0",
											file.status === "uploaded" && "text-green-600"
										)}
									>
										<p
											className={cn(
												"truncate flex-grow",
												file.status === "error" && "text-red-500",
												file.status === "canceled" && "text-amber-500"
											)}
										>
											{file.file.name}
										</p>
										<span className="flex-shrink-0 pl-2">
											({formatFileSize(BigInt(file.file.size))})
										</span>
									</div>
									{!file.status && (
										<div
											role="button"
											className="flex-shrink-0 pl-2"
											onClick={() => handleRemoveFile()}
										>
											<Trash className="w-3 h-3 text-red-400" />
										</div>
									)}
									{file.status === "uploading" && (
										<div
											role="button"
											className="flex-shrink-0 pl-2"
											onClick={() => cancelUpload()}
										>
											<XCircle className="w-3 h-3 text-red-400" />
										</div>
									)}
								</div>
							</div>
						)}
					</div>

					<CardFooter className="pt-10 justify-end">
						<Button
							disabled={isLoading || !file || file.status === "uploaded"}
							onClick={() => handleUpload()}
							className="w-20 h-8 text-sm"
						>
							Upload
						</Button>
					</CardFooter>
				</CardContent>
			</div>
		</Card>
	);
};
