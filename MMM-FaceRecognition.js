Module.register("MMM-FaceRecognition", {
    defaults: {
        updateInterval: 10000, // Update every 10 seconds
        recognizedMessage: "Hello, ",
    },

    start: function() {
        this.sendSocketNotification("START_FACE_RECOGNITION");
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "FACE_RECOGNIZED") {
            this.updateDom();
            this.sendNotification("SHOW_ALERT", { message: "Hello, " + payload.name });
        }
    },

    getDom: function() {
        let wrapper = document.createElement("div");
        wrapper.innerHTML = "Face Recognition Module Active";
        return wrapper;
    }
});