"use client";

import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
} from "@/components/ui/card";
import { useState, useTransition } from "react";
import { Trash, RefreshCw, XCircle } from "lucide-react";
import { Dropzone } from "@/components/file-upload/dropzone";
import { FileWithStatus } from "@/app/types";
import { Spinner } from "@/components/reusable/spinner";
import { cn, formatFileSize } from "@/lib/utils";
// import { Separator } from "@/components/ui/separator";
import { useIsLoading } from "@/hooks/use-is-loading";
import { Button } from "@/components/ui/button";
import { extractText } from "@/app/(landing)/actions/extract-text";

export const FileUploadForm = () => {
	const [file, setFile] = useState<FileWithStatus | null>(null);
	const { isLoading, setIsLoading } = useIsLoading();
	const [isPending, startTransition] = useTransition();

	const updateFileStatus = (
		status: "uploaded" | "error" | "canceled" | "uploading" | "gotPSU"
	) => {
		if (file) {
			setFile((prev) => (prev ? { ...prev, status, isRetrying: false } : null));
		}
	};

	const handleUpload = async () => {
		if (isLoading || !file) return;
		setIsLoading(true);
		updateFileStatus("uploading");

		new Promise<string>((resolve, reject) => {
			const reader = new FileReader();
			reader.readAsDataURL(file.file);
			reader.onload = () => resolve(reader.result as string);
			reader.onerror = reject;
		})
			.then((base64) => {
				startTransition(async () => {
					const result = await extractText(base64);
					console.log(result);
					if (!result.success) {
						throw new Error(result.error);
					}
					console.log("Extracted text:", result.text);
					updateFileStatus("uploaded");
				});
			})
			.catch((error) => {
				console.error("Error:", error);
				updateFileStatus("error");
			})
			.finally(() => {
				setIsLoading(false);
			});
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
			<div className={cn("w-full grid")}></div>
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
											onClick={handleUpload}
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
