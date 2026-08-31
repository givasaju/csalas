document.addEventListener("DOMContentLoaded", function() {
  const data = window.RV_DATA;
  if (!data || !data.nav) return;

  const currentPath = window.location.pathname.split("/").pop() || "index.html";
  const navContainer = document.querySelector(".reversa-doc-nav");

  if (navContainer) {
    navContainer.innerHTML = data.nav.map(item => {
      const isActive = currentPath === item.href || (currentPath === "" && item.href === "index.html");
      return `<a href="${item.href}" data-page-id="${item.id}" class="nav-link ${isActive ? 'active' : ''}" ${isActive ? 'aria-current="page"' : ''}>${item.label}</a>`;
    }).join("");
  }
});
