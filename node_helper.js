const NodeHelper = require("node_helper");
const { PythonShell } = require("python-shell");
const path = require("path");

module.exports = NodeHelper.create({
    start: function() {
        console.log("Starting Face Recognition Module...");
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "START_FACE_RECOGNITION") {
            this.runFaceRecognition();
        }
    },

    runFaceRecognition: function() {
        let pythonProcess = new PythonShell(path.join(__dirname, "MMM-faceRecogition.py"));

        pythonProcess.on("message", (message) => {
            console.log("Face Detected:", message);
            this.sendSocketNotification("FACE_RECOGNIZED", { name: message });
        });

        pythonProcess.end((err) => {
            if (err) console.log("Python error:", err);
        });
    }
});