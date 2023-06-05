import js2py

tf = """
    const URL = "https://teachablemachine.withgoogle.com/models/z8ceXdsVg/";
    let model, labelContainer, maxPredictions, classinfo;

    async function init(event) {
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();

        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) {
            labelContainer.appendChild(document.createElement("div"));
        }
        handleImageUpload(event);
    }

    async function predict(image) {
        if (model) {
            const prediction = await model.predict(image);
            classinfo = console.log(prediction[0].probability.toFixed(2))
            for (let i = 0; i < maxPredictions; i++) {
                const classPrediction =
                    prediction[i].className + ": " + prediction[i].probability.toFixed(2);
                labelContainer.childNodes[i].innerHTML = classPrediction;
            }
        }
    }

    function handleImageUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = async function() {
            const image = new Image();
            image.src = reader.result;
            image.onload = async function() {
                document.getElementById("image-container").innerHTML = "";
                document.getElementById("image-container").appendChild(image);
                await predict(image);
            };
        };
        reader.readAsDataURL(file);
    }
    
    <!--document.getElementById("image-upload").addEventListener("change", init);-->
    init({ target: { files: [new File([], "templates/japanese.jpg")] } });
"""
class_info = js2py.eval_js(tf)
class_info.execute(tf)
print(class_info.classinfo)