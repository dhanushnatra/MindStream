const modelSelect = document.getElementById("modelDropdown");
const changeModel = (newModel) => {
	fetch("/set_model", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ model: newModel }),
	})
		.then((response) => response.json())
		.then((data) => {
			if (data.error) {
				console.error("Error:", data.error);
			} else {
				console.log("Success:", data.message);
				modelSelect.value = newModel; // Update the dropdown to reflect the new model
			}
		})
		.catch((error) => {
			console.error("Error:", error);
		});
};

modelSelect.addEventListener("change", (event) => {
	changeModel(event.target.value);
});
