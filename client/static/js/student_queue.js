setBannerVisibility(true)

const exitQueueButton = document.getElementById("exit-queue")

const exitQueueModal = document.getElementById("self-dequeue-dialog")

exitQueueButton.addEventListener("click", () => showTargetModal(exitQueueModal))

document.getElementById("close-dequeue-dialog").addEventListener("click", () => hideTargetModal(exitQueueModal))

exitQueueModal.addEventListener("close", () => exitQueueModal.style.display = "none")

document.getElementById("submit-self-dequeue").addEventListener("click", () => {
    const reason = document.getElementById("self-dequeue-reason")

    reason.reportValidity()

    if (reason.checkValidity()) {
        fetch("/remove-self-from-queue", {method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"reason": reason.value})}).then(() => {
                hideTargetModal(exitQueueModal)
                fetchPosition()
            }
        )

    }
})

function fetchPosition() {
    fetch("/get-my-position").then(data => {
        return data.json()
    }).then(data => {
        if (data["message"] === undefined) {
            document.getElementById("my-position").textContent = `${data["position"]}`
            setBannerText("You are in the queue!")
            setBannerBad(false);
            exitQueueButton.disabled = false
        } else {
            document.getElementById("my-position").textContent = `N/A`
            setBannerText("You are not in the queue!")
            setBannerBad(true)
            exitQueueButton.disabled = true;
        }
        document.getElementById("queue-length").textContent = `${data["length"]}`
    })
}

function poll() {
    fetchPosition()
    setTimeout(poll, 5000)
}

poll()