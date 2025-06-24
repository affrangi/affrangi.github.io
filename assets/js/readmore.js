document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".readmore").forEach((element) => {
    const maxHeight = parseInt(element.getAttribute("data-max-height") || "200");
    console.log("Max height for readmore element:", maxHeight);
    
    // if the element is taller than the max height, add the read more button
    if (element.scrollHeight > maxHeight) {
      let readMoreButton = document.createElement("button");
      let originalMaxHeight = element.style.maxHeight || `${element.scrollHeight + 60}px`;
      let originalPaddingBottom = element.style.paddingBottom || "0px";
      
      readMoreButton.classList.add("readmore-button");
      readMoreButton.textContent = "Read more";
      element.style.maxHeight = `${maxHeight}px`; 
      
      // Add click event listener to toggle visibility
      readMoreButton.addEventListener("click", function () {
        if (element.classList.contains("expanded")) {
          element.classList.remove("expanded");
          readMoreButton.textContent = "Read more";
          element.style.maxHeight = `${maxHeight}px`; 
          element.style.paddingBottom = originalPaddingBottom; 
          element.style.backgroundImage = "linear-gradient(to bottom, transparent, #fff);"
        } else {
          element.classList.add("expanded");
          readMoreButton.textContent = "Read less";
          element.style.maxHeight = originalMaxHeight;
          element.style.paddingBottom = "60px";
        }
      });
      
      let readMoreContainer = document.createElement("div");
      readMoreContainer.classList.add("readmore-container");

      readMoreContainer.appendChild(readMoreButton);
      element.appendChild(readMoreContainer);
    }
  });
});
