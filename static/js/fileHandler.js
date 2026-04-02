const fileInput = document.getElementById("fileInput");

function triggerFile() {
	fileInput.click();
}

async function handleFileUpload() {
	const file = fileInput.files[0];
	if (file) {
		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch("/upload", {
				method: "POST",
				body: formData,
			});

			if (response.ok) {
				alert("File uploaded successfully!");
				location.reload();
			} else {
				alert("Failed to upload file.");
			}
		} catch (error) {
			console.error("Error uploading file:", error);
			alert("An error occurred while uploading the file.");
		}
	}
}

fileInput.addEventListener("change", handleFileUpload);

async function deleteFile(filename) {
	if (confirm(`Are you sure you want to delete ${filename}?`)) {
		try {
			const response = await fetch(`/delete/${filename}`, {
				method: "DELETE",
			});
			if (response.ok) {
				alert("File deleted successfully!");
				location.reload();
			} else {
				alert("Failed to delete file.");
			}
		} catch (error) {
			console.error("Error deleting file:", error);
			alert("An error occurred while deleting the file.");
		}
	}
}
