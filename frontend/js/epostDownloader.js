// Global Variables
let globalEpostDownloaderRunning = false;

eel.expose(getEpostDownloaderRunning);
function getEpostDownloaderRunning() {
    return globalEpostDownloaderRunning;
};

const getEpostDownloaderDateRange = () => {
    const startDate = document.querySelector("#datepickerEpostDownloaderStart").value;
    const endDate = document.querySelector("#datepickerEpostDownloaderEnd").value;
    return {
        start: startDate,
        end: endDate
    }
};

const getEpostDownloaderDownloadMessageType = () => {
    const allRadioEl = document.querySelector("#downloadAllEpostDownloader");
    return allRadioEl.checked
};

const getEpostDownloaderToken = () => {
 const tokenInputEl = document.querySelector("#epostDownloaderToken");
 return tokenInputEl.value;
};

const startEpostDownloader = async () => {
    toggleLoadingSpinner();
    disableStartButtons();
    clearEpostDownloader();
    showOutputTab();
    showStopButtonEpostDownloader();
    globalEpostDownloaderRunning = true;
    updateMessageCountEpostDownloader(0);

    const token = getEpostDownloaderToken();
    const dateRange = getEpostDownloaderDateRange();
    const downloadAll = getEpostDownloaderDownloadMessageType();
    const categorizeMessages = document.querySelector("#categorizeMessagesEpostDownloader").checked;
    const scrapeEpostConnect = document.querySelector("#scrapeEpostConnectEpostDownloader").checked;

    // User and pass required to login to epost connect website
    const username = getEpostDownloaderUsername();
    const password = getEpostDownloaderPassword();

    let result = null;
    
    try {
        result = await eel.run_epost_downloader(token, username, password, dateRange.start, dateRange.end, downloadAll, categorizeMessages, scrapeEpostConnect)();
    } catch (e) {
        result = "error";
    }

    if (result === "error") {
        showErrorModal("Something went wrong. Please contact support.");
    } else if (result === "error - invalid date") {
        showErrorModal("Invalid date entered.");
    } else if (result === "error - missing epost folder") {
        showErrorModal("Missing the required epost folder.");
    } else if (result === "error - invalid command") {
        showErrorModal("Invalid vtp command.");
    } else if(result === "error - invalid username or password") {
        showErrorModal("Invalid username/password; logon denied");
    } else if (result === "error - missing chromedriver"){
        showErrorModal("Missing the chromedriver.");
    } else if (result === "error - issue with chromedriver") {
        showErrorModal("Issue with the chromedriver.");
    } else if (result === "error - epost connect scrape") {
        showErrorModal("Something went wrong while scraping epost connect.");
    } else if (result === "error - epost connect window closed") {
        showErrorModal("The browser window for epost connect was closed.");
    } else if (result === "error - invalid access token") {
        showErrorModal("Invalid access token.");
    } else if (result === "error - categorizing files") {
        showErrorModal("Something went wrong while categorizing the files.");
    } else if (result === "error - stopped") {
        showErrorModal("Epost Downloader stopped.");
    } else if (result === "error - categorizing files and downloader issue") {
       showCompleteWithErrorModal("Something went wrong while categorizing the files and during the file download, and it may be incomplete.");
    } else if (result === "error - downloader issue") {
        showCompleteWithErrorModal("Something went wrong during the file download, and it may be incomplete.");
    } else if (result === "error - no messages to download") {
        showErrorModal("You have no new messages to download.");
    } else if (result === "success") {
        showCompleteModal();
    }

    hideStopButtonEpostDownloader();
    enableStartButtons();
    toggleLoadingSpinner();
    globalEpostDownloaderRunning = false;
};


const clearEpostDownloader = () => {
    removeEpostDownloaderTabsAndTables();
};

const createEpostDownloaderTable = (id, columnNames, rows, title, numberOfLogs) => {
    // Card
    const cardDiv = document.createElement("div");
    cardDiv.className = "card mt-3 mb-3 epost-downloader-table-card";
    const cardBodyDiv = document.createElement("div");
    cardBodyDiv.className = "card-body";
    const cardHeader = document.createElement("div");
    cardHeader.className = "d-flex justify-content-between";
    const cardTitle = document.createElement("h5");
    cardTitle.className = "card-title mb-3";
    cardTitle.innerHTML = title;
    cardHeader.appendChild(cardTitle);
    // Create excel button
    const excelButton = document.createElement("div");
    excelButton.className = "btn btn-primary excel-button";
    // Add func to excel button
    if (title.toLowerCase().includes("track")) {
        excelButton.onclick = function() {
            exportEpostDownloaderLogToExcel("tracking", numberOfLogs);
        }
    } else if (title.toLowerCase().includes("receive")) {
        excelButton.onclick = function() {
            exportEpostDownloaderLogToExcel("receive", numberOfLogs);
        }
    }

    cardHeader.appendChild(excelButton);
    cardBodyDiv.appendChild(cardHeader);
    const cardTextDiv = document.createElement("div");
    cardTextDiv.className = "card-text";
    // Table
    const table = document.createElement("table");
    table.id = id;
    table.className = "table epost-downloader-table";
    table.style.width = "100%";

    // Thead
    var thead = document.createElement("thead");
    var headerRow = document.createElement("tr");
    thead.style.backgroundColor="#f6f8fa";
    columnNames.forEach((name) => {
        const th = document.createElement("th");
        th.textContent = name;
        th.style.color="#1f2328";
        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);
    // Tbody
    const tbody = document.createElement("tbody");

    for (let i = 0; i < rows.length; i++) {
        // Skip the rows with null attachments - they are not useful
        if (rows[i][5] !== "null") {
            const tr = document.createElement("tr");

            if (title === "VTP Receive Log") {
                if (rows[i][6] === "Failure") {
                    tr.style.backgroundColor = "#ffc2ad";
                } else if (rows[i][6] === "Success") {
                    tr.style.backgroundColor = "#adffc2";
                }
            }
            
            for (let j = 0; j < rows[i].length; j++) {
                const td = document.createElement("td");
                td.textContent = rows[i][j];
                tr.appendChild(td);
            }

            tbody.appendChild(tr); 
        }     
    }

    table.appendChild(tbody);
    cardTextDiv.appendChild(table);
    cardBodyDiv.appendChild(cardTextDiv);
    cardDiv.appendChild(cardBodyDiv);
    return cardDiv;
};

eel.expose(addTableToTabEpostDownloader);
function addTableToTabEpostDownloader(tableId, title, columnNames, rows, numberOfLogs) {
    const table = createEpostDownloaderTable(tableId, columnNames, rows, title, numberOfLogs);
    tabElement = document.querySelector("#navEpostDownloaderLogsTab");
    tabElement.style.display = "block";

    document.querySelector("#navEpostDownloaderLogs").appendChild(table);
    new DataTable(`#${tableId}`,{
        scrollX: true,
        pageLength: 5,
        lengthMenu: [
            [5, 10, 25, 50, -1],
            [5, 10, 25, 50, 'All']
        ]
     });
};

/**
 * Removes tables from the Epost Downloader interface.
 * Iterates through all table elements with class "epost-downloader-table-card" and removes them from the DOM.
 */
const removeEpostDownloaderTables = () => {
    document.querySelectorAll(".epost-downloader-table-card").forEach((element) => element.remove());
};

/**
 * Removes tabs from the Epost Downloader interface, except the Download tab.
 * Hides tabs by setting their display style to "none".
 */
const removeEpostDownloaderTabs = () => {
    document.querySelectorAll(".epost-downloader-tab").forEach((element) => {
        if (element.id !== "navEpostDownloaderDownloadTab") {
            element.style.display = "none";
        }
    });
};

/**
 * Removes tabs and tables from the Epost Downloader interface.
 */
const removeEpostDownloaderTabsAndTables = () => {
    clearTextAreaEpostDownloader();
    removeEpostDownloaderTabs();
    removeEpostDownloaderTables();
};

const showOutputTab = () => {
    const tabEl = document.querySelector("#navEpostDownloaderOutputTab");
    tabEl.style.display = "block";
};

/**
 * Updates the text area in the epost downloader.
 * @param {string} newText - The new text to append to the text area.
 */
eel.expose(handleUpdateTextAreaEpostDownloader);
function handleUpdateTextAreaEpostDownloader(newText) {
    const textAreaElement = document.querySelector("#textAreaEpostDownloader");
    textAreaElement.value += newText;
    textAreaElement.scrollTop = textAreaElement.scrollHeight;
};

const clearTextAreaEpostDownloader = () => {
    const textAreaElement = document.querySelector("#textAreaEpostDownloader");
    textAreaElement.value = "";
};

const showStopButtonEpostDownloader = () => {
    const buttonEl = document.querySelector("#stopButtonEpostDownloader");
    buttonEl.style.display = "block";
};

const hideStopButtonEpostDownloader = () => {
    const buttonEl = document.querySelector("#stopButtonEpostDownloader");
    buttonEl.disabled = false;
    buttonEl.style.display = "none";
};

const disableStopButtonEpostDownloader = () => {
    const buttonEl = document.querySelector("#stopButtonEpostDownloader");
    buttonEl.disabled = true;
};

const stopEpostDownloader = () => {
    globalEpostDownloaderRunning = false;
    disableStopButtonEpostDownloader();
};

/**
 * Updates the current message count for the Epost Downloader UI.
 * @param {number} count - The current number of messages to be displayed.
 */
eel.expose(updateMessageCountEpostDownloader);
function updateMessageCountEpostDownloader(count) {
    document.querySelector("#epostDownloaderMessageCount").textContent = count;
};

/*
 * Export Epost Downloader log data to an Excel file.
 * 
 * @param {string} logType - The type of logs to download. Should be one of "tracking" or "receive".
 * @param {number} numberOfLogs - The number of logs to include in the Excel file.
 */
const exportEpostDownloaderLogToExcel = async (logType, numberOfLogs) => {
    toggleLoadingSpinner();
    let result = "error";

    if (logType === "tracking") {
        result = await eel.export_track_logs_excel(numberOfLogs)();
    } else if (logType === "receive") {
        result = await eel.export_receive_logs_excel(numberOfLogs)();
    }

    if (result === "error") {
        showErrorModal("Something went wrong. Please contact support.")
    } else if (result === "success") {
        showCompleteModal();
    }
    toggleLoadingSpinner();
};


/**
 * Handles the click event of the 'scrapeEpostConnectEpostDownloader' checkbox.
 * If the checkbox is checked, displays the 'epostDownloaderUserPassInputGroup';
 * otherwise, hides it.
 */
const handleScrapeEpostConnectCheckedEpostDownloader = () => {
    const isChecked = document.querySelector("#scrapeEpostConnectEpostDownloader").checked;

    if (isChecked) {
        document.querySelector("#epostDownloaderUserPassInputGroup").style.display = "block";
    } else if (!isChecked) {
        document.querySelector("#epostDownloaderUserPassInputGroup").style.display = "none";
    }
};

/**
 * Retrieves the value of the epostDownloaderUsername input field.
 * @returns {string} The value of the epostDownloaderUsername input field.
 */
const getEpostDownloaderUsername = () => {
    return document.querySelector("#epostDownloaderUsername").value;
};

/**
 * Retrieves the value of the epostDownloaderPassword input field.
 * @returns {string} The value of the epostDownloaderPassword input field.
 */
const getEpostDownloaderPassword = () => {
    return document.querySelector("#epostDownloaderPassword").value;
};