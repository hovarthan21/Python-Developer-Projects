
document.addEventListener("DOMContentLoaded", () => {
  const selects = document.querySelectorAll("select");

  selects.forEach(select => {
    const searchBox = document.createElement("input");
    searchBox.type = "text";
    searchBox.placeholder = "Search...";
    searchBox.style.marginBottom = "10px";
    select.parentNode.insertBefore(searchBox, select);

    searchBox.addEventListener("keyup", () => {
      const filter = searchBox.value.toLowerCase();
      const options = select.options;
      for (let i = 0; i < options.length; i++) {
        const txt = options[i].text.toLowerCase();
        options[i].style.display = txt.includes(filter) ? "" : "none";
      }
    });
  });
});
