"use client";

import { ModeToggle } from "@/components/mode-toggle";
import { cn } from "@/lib/utils";
// import dynamic from "next/dynamic";
import { Logo } from "./logo";

export const Navbar = () => {
	return (
		<div
			className={cn(
				"h-16 z-50 fixed top-0 flex items-center w-full p-2 sm:p-6 backdrop-blur"
			)}
		>
			<Logo showText={true} />

			<div className="ml-auto justify-end w-full flex items-center gap-x-5">
				{/* <FileUploadButton>
					<Button size="sm">Upload</Button>
				</FileUploadButton> */}
				<div className="flex flex-row gap-x-5 items-center">
					<ModeToggle />
				</div>
			</div>
		</div>
	);
};
