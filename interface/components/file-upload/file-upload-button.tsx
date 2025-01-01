"use client";

import {
	Dialog,
	DialogContent,
	DialogTrigger,
	DialogTitle,
} from "@/components/ui/dialog";
import { FileUploadForm } from "./file-upload-form";
import { useState } from "react";

interface LoginButtonProps {
	children: React.ReactNode;
	mode?: "modal" | "redirect";
	asChild?: boolean;
}

export const FileUploadButton = ({
	children,
	mode = "redirect",
	asChild,
}: LoginButtonProps) => {
	const [open, setOpen] = useState(false);

	if (mode === "modal") {
		return (
			<Dialog open={open} onOpenChange={setOpen}>
				<DialogTrigger asChild={asChild}>{children}</DialogTrigger>
				<DialogContent className="p-0 bg-transparent border-none rounded-lg">
					<DialogTitle className="sr-only">Upload File</DialogTitle>
					<FileUploadForm />
				</DialogContent>
			</Dialog>
		);
	}

	return <span className="cursor-pointer">{children}</span>;
};
