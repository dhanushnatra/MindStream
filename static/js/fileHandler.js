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

const question = document.getElementById("textInput");
const messages = document.querySelector(".messages");

async function askQuestion() {
	if (question.value.trim() === "") {
		alert("Please enter a question.");
		return;
	}

	try {
		const userDiv = document.createElement("div");
		userDiv.className = "userMsg";
		userDiv.textContent = question.value;
		messages.appendChild(userDiv);

		const response = await fetch("/question", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ question: question.value }),
		});

		const loadingDiv = document.createElement("div");
		loadingDiv.className = "loading";
		loadingDiv.innerHTML = "Generating response...";
		messages.appendChild(loadingDiv);

		if (response.ok) {
			const data = await response.json();

			messages.removeChild(loadingDiv);

			const audio = document.createElement("audio");
			audio.controls = true;

			const source = document.createElement("source");
			source.src = data.audio_url;
			source.type = "audio/wav";

			audio.appendChild(source);

			audio.appendChild(
				document.createTextNode(
					"Your browser does not support the audio element.",
				),
			);

			messages.appendChild(audio);

			document.getElementById("textInput").value = "";

			messages.scrollTop = messages.scrollHeight;
		} else {
			alert("Failed to get an answer.");
		}
	} catch (error) {
		console.error("Error asking question:", error);
		alert("An error occurred while asking the question.");
	}
}

question.addEventListener("keypress", function (event) {
	if (event.key === "Enter") {
		event.preventDefault();
		askQuestion();
	}
});
