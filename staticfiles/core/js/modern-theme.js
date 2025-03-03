// Modern Premium Theme JS for PR Tracker
// Created by Claude AI - Premium UI Kit

document.addEventListener("DOMContentLoaded", function () {
  // Add fade-in animation to cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    card.classList.add("fade-in");
    card.style.animationDelay = `${index * 0.1}s`;
  });

  // Enhance hover effects on action cards
  const actionCards = document.querySelectorAll(".action-card");
  actionCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      const iconBox = this.querySelector(".icon-box");
      if (iconBox) {
        iconBox.style.transform = "scale(1.1)";
      }
    });

    card.addEventListener("mouseleave", function () {
      const iconBox = this.querySelector(".icon-box");
      if (iconBox) {
        iconBox.style.transform = "scale(1)";
      }
    });
  });

  // Add subtle parallax effect to welcome section
  const welcomeSection = document.querySelector(".welcome-section");
  if (welcomeSection) {
    window.addEventListener("scroll", function () {
      const scrollPosition = window.scrollY;
      if (scrollPosition < 300) {
        welcomeSection.style.backgroundPosition = `center ${
          scrollPosition * 0.05
        }px`;
      }
    });
  }

  // Enhance buttons with hover effects
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach((button) => {
    button.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-2px)";
    });

    button.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // Add counter animation to statistics
  const statNumbers = document.querySelectorAll(".stats-card .display-6");
  statNumbers.forEach((stat) => {
    const finalValue = parseInt(stat.textContent.replace(/[^\d]/g, ""), 10);
    if (!isNaN(finalValue)) {
      animateCounter(stat, 0, finalValue, 1500);
    }
  });

  // Add ripple effect to buttons
  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("click", createRipple);
  });

  // Add smooth scrolling to anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId !== "#" && document.querySelector(targetId)) {
        e.preventDefault();
        document.querySelector(targetId).scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });

  // Initialize tooltips if Bootstrap JS is loaded
  if (typeof bootstrap !== "undefined" && bootstrap.Tooltip) {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // Initialize popovers if Bootstrap JS is loaded
  if (typeof bootstrap !== "undefined" && bootstrap.Popover) {
    const popoverTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  }

  // Add data-bs-toggle attributes to elements that need them
  document.querySelectorAll(".btn-info, .btn-warning").forEach((btn) => {
    if (
      !btn.getAttribute("data-bs-toggle") &&
      !btn.getAttribute("data-toggle")
    ) {
      btn.setAttribute("data-bs-toggle", "tooltip");
      btn.setAttribute("data-bs-placement", "top");
      if (!btn.getAttribute("title")) {
        btn.setAttribute("title", btn.textContent.trim());
      }
    }
  });
});

// Helper function for counter animation
function animateCounter(element, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const currentValue = Math.floor(progress * (end - start) + start);

    // Preserve any currency symbols or other characters
    const originalText = element.textContent;
    const currencySymbol = originalText.replace(/[\d,.\s]/g, "");

    element.textContent = currencySymbol + currentValue.toLocaleString();

    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      element.textContent = originalText; // Ensure final value is exactly as it should be
    }
  };
  window.requestAnimationFrame(step);
}

// Helper function for button ripple effect
function createRipple(event) {
  const button = event.currentTarget;

  const circle = document.createElement("span");
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  circle.style.width = circle.style.height = `${diameter}px`;
  circle.style.left = `${
    event.clientX - button.getBoundingClientRect().left - radius
  }px`;
  circle.style.top = `${
    event.clientY - button.getBoundingClientRect().top - radius
  }px`;
  circle.classList.add("ripple");

  const ripple = button.querySelector(".ripple");
  if (ripple) {
    ripple.remove();
  }

  button.appendChild(circle);
}

// Add responsive behavior for tables
function makeTablesResponsive() {
  const tables = document.querySelectorAll("table");
  tables.forEach((table) => {
    if (!table.parentElement.classList.contains("table-responsive")) {
      const wrapper = document.createElement("div");
      wrapper.classList.add("table-responsive");
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });
}

// Initialize responsive tables
document.addEventListener("DOMContentLoaded", makeTablesResponsive);
