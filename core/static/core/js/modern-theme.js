/**
 * Modern Theme JavaScript
 * Enhances the PR Tracker UI with modern interactions and functionality
 */

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Add shadow to navbar on scroll
  window.addEventListener("scroll", function () {
    const navbar = document.querySelector(".navbar");
    if (window.scrollY > 10) {
      navbar.classList.add("navbar-scrolled");
    } else {
      navbar.classList.remove("navbar-scrolled");
    }
  });

  // Enhance form inputs with floating labels
  const formInputs = document.querySelectorAll(".form-control");
  formInputs.forEach((input) => {
    input.addEventListener("focus", () => {
      input.parentElement.classList.add("focused");
    });

    input.addEventListener("blur", () => {
      if (!input.value) {
        input.parentElement.classList.remove("focused");
      }
    });

    // Initialize state for inputs with values
    if (input.value) {
      input.parentElement.classList.add("focused");
    }
  });

  // File upload enhancement
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    const fileLabel = input.nextElementSibling;
    if (fileLabel && fileLabel.classList.contains("custom-file-label")) {
      input.addEventListener("change", () => {
        let fileName = input.files[0]?.name || "Choose file";
        fileLabel.textContent = fileName;
      });
    }
  });

  // Add animation to cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.classList.add("card-hover");
    });

    card.addEventListener("mouseleave", () => {
      card.classList.remove("card-hover");
    });
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      if (targetId !== "#") {
        document.querySelector(targetId).scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });

  // Dropdown menu enhancement
  const dropdownItems = document.querySelectorAll(".dropdown-item");
  dropdownItems.forEach((item) => {
    item.addEventListener("mouseenter", () => {
      item.classList.add("active");
    });

    item.addEventListener("mouseleave", () => {
      item.classList.remove("active");
    });
  });

  // Dashboard chart animations (if charts exist)
  if (typeof Chart !== "undefined") {
    Chart.defaults.animation.duration = 2000;
    Chart.defaults.animation.easing = "easeOutQuart";
  }

  // Handle publication and edition fields in Coverage form
  const publicationSelect = document.getElementById("id_publication");
  const editionSelect = document.getElementById("id_edition");

  if (publicationSelect && editionSelect) {
    publicationSelect.addEventListener("change", function () {
      const publicationId = this.value;

      // Clear current options
      editionSelect.innerHTML = '<option value="">---------</option>';

      if (publicationId) {
        // Use the proper URL pattern instead of hardcoded path
        const editionsUrl = `/get-editions/?publication_id=${publicationId}`;

        // Fetch editions for the selected publication
        fetch(editionsUrl)
          .then((response) => response.json())
          .then((data) => {
            data.editions.forEach((edition) => {
              const option = document.createElement("option");
              option.value = edition.id;
              option.textContent = edition.name;
              editionSelect.appendChild(option);
            });
          })
          .catch((error) => console.error("Error fetching editions:", error));
      }
    });
  }

  // Handle client and campaign fields in Coverage form
  const clientSelect = document.getElementById("id_client");
  const campaignSelect = document.getElementById("id_campaign");

  if (clientSelect && campaignSelect) {
    clientSelect.addEventListener("change", function () {
      const clientId = this.value;

      // Clear current options
      campaignSelect.innerHTML = '<option value="">---------</option>';

      if (clientId) {
        // Use the proper URL pattern instead of hardcoded path
        const campaignsUrl = `/get-campaigns/?client_id=${clientId}`;

        // Fetch campaigns for the selected client
        fetch(campaignsUrl)
          .then((response) => response.json())
          .then((data) => {
            data.campaigns.forEach((campaign) => {
              const option = document.createElement("option");
              option.value = campaign.id;
              option.textContent = campaign.name;
              campaignSelect.appendChild(option);
            });
          })
          .catch((error) => console.error("Error fetching campaigns:", error));
      }
    });
  }

  // File upload preview
  const fileUploadInput = document.querySelector(".file-upload-input");
  if (fileUploadInput) {
    fileUploadInput.addEventListener("change", function (e) {
      const fileDetails = document.getElementById("file-details");
      const fileNameElement = document.getElementById("file-name");
      const fileSizeElement = document.getElementById("file-size");

      if (this.files.length > 0) {
        const file = this.files[0];
        const fileSize = (file.size / 1024).toFixed(2) + " KB";

        if (fileNameElement) fileNameElement.textContent = file.name;
        if (fileSizeElement) fileSizeElement.textContent = fileSize;
        if (fileDetails) fileDetails.classList.remove("d-none");
      }
    });
  }

  // Initialize Select2 if jQuery and Select2 are available
  if (
    typeof jQuery !== "undefined" &&
    typeof jQuery.fn.select2 !== "undefined"
  ) {
    jQuery(document).ready(function ($) {
      $(".select2").select2({
        theme: "bootstrap-5",
        width: "100%",
      });
    });
  }

  console.log("Modern theme JS initialized");
});
