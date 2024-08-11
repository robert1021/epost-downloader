
/**
 * Event listener triggered when the DOM content is loaded.
 * Fetches the application information and updates various elements accordingly.
 */
document.addEventListener("DOMContentLoaded", async function () {
    const appInfo = await eel.handle_app_info()();
    document.title = `${appInfo.name} v${appInfo.version}`;
    document.querySelector("#appName").innerHTML = `${appInfo.name} v${appInfo.version}`;
    document.querySelector("#buildDate").innerHTML = appInfo.build;

    // Initialize date pickers
    flatpickr("#datepicker");
    flatpickr("#datepickerNhpsas");
    flatpickr("#datePickerIts", {
        dateFormat: 'Y-m',
    });
    flatpickr("#datepickerEpostDownloaderStart", {
        dateFormat: 'm/d/Y',
    });
    flatpickr("#datepickerEpostDownloaderEnd", {
        dateFormat: 'm/d/Y',
    });

});

// Remove quotes from start and end of file path that gets pasted into certain inputs.
document.querySelectorAll(".filepath-input").forEach((element) => {
    element.addEventListener("paste", (event) => {
        event.preventDefault();
        let contents = event.clipboardData.getData('text');
        if (contents.length > 0) {
            if (contents.startsWith('"')) {
                contents = contents.substr(1, contents.length);
            }
            if (contents.endsWith('"')) {
                contents = contents.substr(0, contents.length - 1);
            }
        }
        element.value = element.value + contents;
    })
});

const setNavbarTitle = (text) => {
    document.querySelector("#navbarTitle").textContent = text;
};

/**
 * Show or hide pages and sidebar tiles based on the provided page ID.
 * @param {string} pageId - The ID of the page to show.
 */
const showPage = (pageId) => {
    const pages = document.querySelectorAll(".page");
    const sideBarTiles = document.querySelectorAll(".sidebar-tile");
    const homeButtonElement = document.querySelector("#homeButton");
    const helpButtonElement = document.querySelector("#helpButton");

    if (pageId === "epost-downloader") {
        homeButtonElement.style.display = "none";
    } else {
        homeButtonElement.style.display = "block";
    }

    if (pageId === "help") {
        helpButtonElement.style.display = "none";
    } else {
        helpButtonElement.style.display = "block";
    }

    sideBarTiles.forEach((element) => {
        element.classList.remove("sidebar-tile-selected");
    });

    if (pageId === "epost-downloader") {
        document.querySelector("#sidebarTileEpostDownloader").classList.add("sidebar-tile-selected");
        setNavbarTitle("ePost Downloader");
    } else if (pageId === "help") {
        document.querySelector("#sideBarTileHelp").classList.add("sidebar-tile-selected");
        setNavbarTitle("Help");
    }

    pages.forEach((page) => {
        if (page.id === pageId) {
            page.style.display = "block";
        } else {
            page.style.display = "none";
        }
    });

};

/**
 * Toggle the visibility of the loading spinner element.
 */
const toggleLoadingSpinner = () => {
    const spinnerElement = document.querySelector("#loadingSpinner");
    if (spinnerElement.style.display === "block") {
        spinnerElement.style.display = "none";
    } else {
        spinnerElement.style.display = "block";
    }
};

/**
 * Show the complete modal dialog.
 */
const showCompleteModal = () => {
    const modal = new bootstrap.Modal(
        document.querySelector("#completeModal")
    );
    modal.show();
};

/**
 * Show the error modal dialog with an optional error message.
 * @param {string} [errorMessage=""] - The error message to display in the modal.
 */
const showErrorModal = (errorMessage = "") => {
    const modal = new bootstrap.Modal(
        document.querySelector("#errorModal")
    );
    document.querySelector("#errorModalBody").innerHTML = errorMessage;
    modal.show();
};

/**
 * Show the error modal dialog with an optional error message.
 * @param {string} [errorMessage=""] - The error message to display in the modal.
 */
const showCompleteWithErrorModal = (errorMessage = "") => {
    const modal = new bootstrap.Modal(
        document.querySelector("#completeWithErrorModal")
    );
    document.querySelector("#completeWithErrorModalBody").innerHTML = errorMessage;
    modal.show();
};

/**
 * Show the failsafe modal dialog.
 */
const showFailsafeModal = () => {
    const modal = new bootstrap.Modal(
        document.querySelector("#failsafeModal")
    );
    modal.show();
};

/**
 * Opens a file dialog using eel and sets the selected file path to the specified input element.
 * @param {string} inputId - The ID of the input element where the selected file path will be set.
 */
const openFiledialog = async (inputId) => {
    const result = await eel.handle_open_filedialog()();
    const pathInput = document.querySelector(`#${inputId}`);
    pathInput.value = result;
};

/**
 * Opens a directory dialog using eel and sets the selected directory path to the specified input element.
 * @param {string} inputId - The ID of the input element where the selected directory path will be set.
 */
const openDirectory = async (inputId) => {
    const result = await eel.handle_open_directory()();
    const pathInput = document.querySelector(`#${inputId}`);
    pathInput.value = result;
};

/**
 * Updates the progress bar with the specified ID by incrementing its value.
 * @param {string} progressBarId - The ID of the progress bar element.
 * @param {number} increment - The amount by which to increment the progress bar value.
 */
eel.expose(handleUpdateProgressBar);
function handleUpdateProgressBar(progressBarId, increment) {
    const progressBarElement = document.querySelector(`#${progressBarId}`);
    let valueNow = parseFloat(progressBarElement.ariaValueNow);
    let newValue = valueNow + increment;
    progressBarElement.setAttribute("aria-valuenow", newValue);
    progressBarElement.style.width = newValue + "%";
}

/**
 * Resets the progress bar with the specified ID to its initial state.
 * @param {string} progressBarId - The ID of the progress bar element.
 */
const resetProgressbar = (progressBarId) => {
    const progressBarElement = document.querySelector(`#${progressBarId}`);
    progressBarElement.setAttribute("aria-valuenow", "0");
    progressBarElement.style.width = 0 + "%";
};

/**
 * Sets the progress bar with the specified ID to its completed state (100%).
 * @param {string} progressBarId - The ID of the progress bar element.
 */
const completeProgressbar = (progressBarId) => {
    const progressBarElement = document.querySelector(`#${progressBarId}`);
    progressBarElement.setAttribute("aria-valuenow", "100");
    progressBarElement.style.width = 100 + "%";
};

/**
 * Enables all start buttons by removing the "disabled" attribute.
 */
const enableStartButtons = () => {
    document.querySelectorAll(".start-button").forEach((element) => {
        element.disabled = false;
    });
};

/**
 * Disables all start buttons by setting the "disabled" attribute to true.
 */
const disableStartButtons = () => {
    document.querySelectorAll(".start-button").forEach((element) => {
        element.disabled = true;
    });
};

/**
 * Adjusts the column headers of DataTables to fit the content properly.
 */
const fixTableColumnHeaders = () => {
    $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
};