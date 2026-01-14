const visitModal = document.getElementById("visit")

// visitModal.style.display = "flex"
// visitModal.showModal()

visitModal.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        e.preventDefault()
    }
})

visitModal.addEventListener("close", () => {
    visitModal.style.display = "none"
})

function setVisit(info) {
    const name = info["preferred_name"]
    const ubit = info["username"]
    const studentReason = info["reason"]
    const visitID = info["visitID"]

    console.log(info)

    const taReason = document.getElementById("ta-visit-notes")

    document.getElementById("visit-student-name").textContent = name
    document.getElementById("visit-student-email").textContent = `${ubit}@buffalo.edu`
    document.getElementById("student-visit-reason").textContent = studentReason

    document.getElementById("end-visit").onclick = () => {

        taReason.reportValidity()

        if (taReason.checkValidity()) {
            fetch("/end-visit", {
            method: "POST",
            body: JSON.stringify({"id": visitID, "reason": taReason.value}),
            headers: {"Content-Type": "application/json"}
            }).then(
                () => hideTargetModal(visitModal)
            )
        }
    }

}