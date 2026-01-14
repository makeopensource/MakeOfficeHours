// Banner handling functions; i.e. "You are not in the queue!"


const banner = document.getElementById("queue-banner")
let bannerBad = false;
let bannerVisible = false;


function setBannerVisibility(to) {
    bannerVisible = to;
    if (to) {
        banner.className = `${bannerBad ? "bad" : ""}`
    } else {
        banner.className = "disabled"
    }
}

function setBannerText(to) {
    banner.textContent = to;
}

function setBannerBad(to) {
    bannerBad = to;
    if (bannerVisible && bannerBad) {
        banner.className = "bad"
    } else if (bannerVisible) {
        banner.className = ""
    }
}

// Return info of the currently logged-in user.
// null if the user isn't logged in at all
async function getMyInfo() {
    const res= await fetch("/me")
    if (!res.ok) {
        return null;
    }
    return res.json()
}

// Return info of the requested user
// Only works if the user is logged in as
// TA or higher.
async function getUserInfo(user) {
    const res = await fetch (`/user/${user}`)
    if (!res.ok) {
        return null;
    }
    return res.json()
}

// Modal stuff

function showTargetModal(target) {
    target.style.display = "flex"
    target.showModal()
}

function hideTargetModal(target) {
    target.style.display = "none"
    target.close()
}