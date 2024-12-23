document.addEventListener("DOMContentLoaded", () => {
  const generateButton = document.getElementById("generateButton");
  const promptInput = document.getElementById("promptInput");
  const dropdown1 = document.getElementById("dropdown1");
  const dropdown2 = document.getElementById("dropdown2");

  let selectedReferenceText = "";
  let selectedReferenceValue = "";

  generateButton.addEventListener("click", () => {
  
    const promptValue = promptInput.value;
    const dropdown1Value = dropdown1.value;
    const dropdown2Value = dropdown2.value;

    console.log("Dropdown 1 Value:", dropdown1Value);
    console.log("Dropdown 2 Value:", dropdown2Value);
    console.log("Selected Reference Text:", selectedReferenceText);
    console.log("Selected Reference Value:", selectedReferenceValue);

    fetch("http://localhost:8000/api/data", {
      redirect: "follow",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: promptValue }),
    })
      .then((response) => {
        window.location.href = response.url
      })
      .then((data) => {
        console.log("Success:", data);
        
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

  const galleryThumbnails = document.querySelectorAll(".gallery-thumbnail");
  galleryThumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener("click", () => {

      galleryThumbnails.forEach((th) => th.classList.remove("selected"));

   
      thumbnail.classList.add("selected");


      selectedReferenceText = thumbnail.querySelector("p").textContent;
      selectedReferenceValue = thumbnail.getAttribute("data-value");


      console.log("Selected Reference Material:");
      console.log("Text:", selectedReferenceText);
      console.log("Value:", selectedReferenceValue);
    });
  });
});
