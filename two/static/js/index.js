document.addEventListener("DOMContentLoaded", () => {
    const menuIcon = document.getElementById("menuicn");
    const navContainer = document.querySelector(".navcontainer");
    const mainContainer = document.querySelector(".main");

    if (menuIcon && navContainer) {
        menuIcon.addEventListener("click", () => {
            navContainer.classList.toggle("navclose");
            if(mainContainer) {
                mainContainer.classList.toggle("main-shift");
            }
        });
    }
});

/**
 * Global API Fetch Helper in case you want to pull data programmatically later
 */
async function fetchFromApi(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error(`HTTP Error! Status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("API Fetch Failure on endpoint:", endpoint, error);
        return null;
    }
}