setBannerVisibility(true);
setBannerText("You are not clocked in! Clock in to broadcast your availability to students.")
setBannerBad(true);


getMyInfo().then(info => {
    if (info == null) {
        window.location = "/"
    }
    document.getElementById("welcome-text").textContent = `Hello, ${info["preferred_name"]}!`
})

// Force enqueue modal

const enqueueDialog = document.getElementById("force-enqueue-dialog")

document.getElementById("enqueue-dialog-button").addEventListener("click", () => {
    enqueueDialog.style.display = "flex"
    document.getElementById("force-enqueue").value = ""
    enqueueDialog.showModal()
    document.getElementById("enqueue-error-message").textContent = ""
})

document.getElementById("close-enqueue-dialog").addEventListener("click", () => {
    enqueueDialog.close()
})

enqueueDialog.addEventListener("close", () => {
    enqueueDialog.style.display = "none"
})

// Clear queue modal

const clearQueueDialog = document.getElementById("clear-queue-dialog")

document.getElementById("clear-queue-dialog-button").addEventListener("click", () => {
    showTargetModal(clearQueueDialog)
    document.getElementById("clear-queue-error-message").textContent = ""
})

document.getElementById("clear-queue-confirm").addEventListener("click", () => {
    fetch("/clear-queue", {method: "DELETE"}).then(res => {
        if (res.ok) {
            clearQueueDialog.close()
            setTimeout(fetchQueue, 50)
        }
        return res.json()
    }).then(json => {
            document.getElementById("clear-queue-error-message").textContent = json["message"]
    })})

document.getElementById("clear-queue-cancel").addEventListener("click", () => hideTargetModal(clearQueueDialog))

clearQueueDialog.addEventListener("close", () => {clearQueueDialog.style.display = "none"})

document.getElementById("submit-force-enqueue").onclick = () => {
    fetch("/enqueue-ta-override", {method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"identifier": document.getElementById("force-enqueue").value})}).then(res => {
            if (res.ok) {
                enqueueDialog.close()
                setTimeout(fetchQueue, 50)
            }
            return res.json()
        }).then(json => {
            document.getElementById("enqueue-error-message").textContent = json["message"]
    })
}

const queueContainer = document.getElementById("queue-container")

function addQueueEntry(student) {
    let entry = document.createElement("div")
    entry.className = "queue-entry"


    let entryInfo = document.createElement("div")
    entryInfo.className = "queue-entry-info"
    entryInfo.textContent = `${student["preferred_name"]} (${student["ubit"]})`

    let entryButtons = document.createElement("div")
    entryButtons.className = "queue-entry-buttons"
    let startVisitButton = document.createElement("button")
    startVisitButton.textContent = "Start Visit"

    startVisitButton.onclick = () => {
        fetch("/help-a-student", {
            method: "POST",
            body: JSON.stringify({"id": student["id"]}),
            headers: {"Content-Type": "application/json"}
        }).then((res) => {
            return res.json()
        }).then(data => {
            setVisit(data)
            showTargetModal(visitModal)
        })
    }

    let removeButton = document.createElement("button")
    removeButton.textContent = "Remove"
    let moveToEndButton = document.createElement("button")
    moveToEndButton.textContent = "Move to End"

    entryButtons.append(startVisitButton, removeButton, moveToEndButton)

    entry.append(entryInfo, entryButtons)

    queueContainer.append(entry)
}

function fetchQueue() {
    fetch("/get-queue").then(data => {
        return data.json()
    }).then(data => {
        queueContainer.innerHTML = ''

        for (let entry of data) {
            addQueueEntry(entry)
        }


        if (queueContainer.children.length > 0) {
            document.getElementById("student-count-text").textContent = `${queueContainer.children.length} students in the queue.`
            queueContainer.children[0].className = queueContainer.children[0].className + " top"
        } else {
            document.getElementById("student-count-text").textContent = "The queue is empty!"
        }
    })
}

function poll() {
    fetchQueue()
    setTimeout(poll, 5000)
}

poll()




