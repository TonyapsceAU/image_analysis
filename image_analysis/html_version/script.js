class Quadtree {
    constructor() {
      this.images = [];
      this.divided = false;
      this.northeast = null;
      this.northwest = null;
      this.southeast = null;
      this.southwest = null;
    }
  
    checkImg(image, x, y) {
      if (predict(image)>0.5) {
        const { width: w, height: h } = image;
        this.images.push({ image, x, y, w, h });
      } else {
        if (!this.divided) {
          const images = this.subdivide(image, x, y);
        }
  
        const w = image.width;
        const h = image.height;
  
        if (this.northeast.checkImg(this.images[0], x + w / 2, y)) {
          return true;
        } else if (this.northwest.checkImg(this.images[1], x, y)) {
          return true;
        } else if (this.southeast.checkImg(this.images[2], x + w / 2, y + h / 2)) {
          return true;
        } else if (this.southwest.checkImg(this.images[3], x, y + h / 2)) {
          return true;
        }
      }
    }
  
    subdivide(image, x, y) {
      const { width: w, height: h } = image;
  
      this.northeast = new Quadtree();
      this.northwest = new Quadtree();
      this.southeast = new Quadtree();
      this.southwest = new Quadtree();
  
      this.divided = true;
    
      this.images = this.divideImage(image);

    }

    divideImage(inputImage) {
        let middleX, middleY;
        let outputImages = [];
      
        inputImage.onload = function() {
          middleX = inputImage.width / 2;
          middleY = inputImage.height / 2;
      
          // Create a canvas to draw the image
          let canvas = document.createElement('canvas');
          let context = canvas.getContext('2d');
          canvas.width = inputImage.width;
          canvas.height = inputImage.height;
          context.drawImage(inputImage, 0, 0);
      
          // Top-left quadrant
          let topLeftImage = context.getImageData(0, 0, middleX, middleY);
          outputImages.push(topLeftImage);
      
          // Top-right quadrant
          let topRightImage = context.getImageData(middleX, 0, middleX, middleY);
          outputImages.push(topRightImage);
      
          // Bottom-left quadrant
          let bottomLeftImage = context.getImageData(0, middleY, middleX, middleY);
          outputImages.push(bottomLeftImage);
      
          // Bottom-right quadrant
          let bottomRightImage = context.getImageData(middleX, middleY, middleX, middleY);
          outputImages.push(bottomRightImage);
        };
      
        return outputImages;
      }

  }
  

var images_path = [];
var currentIndex = 0;
var quadtree;
var count = 0
const url = "https://teachablemachine.withgoogle.com/models/z8ceXdsVg/";
let model, maxPredictions;

async function init() {
    const modelURL = url + "model.json";
    const metadataURL = url + "metadata.json";

    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();
}

async function predict(image, labelContainer) {
    if (model) {
        const prediction = await model.predict(image);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction =
                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }
    }
}

function checkWord(a){
    if(count==0){
        count += 1
        return false;
    }else{
        return true;
    }
}


function load_images_paths(event) {
    images_path = Array.from(event.target.files);
    currentIndex = 0;

    var folderPath = event.target.files[0].webkitRelativePath.split("/").slice(0, -1).join("/");
    var folderName = folderPath.substring(folderPath.lastIndexOf("/") + 1);

    document.getElementById('startButton').disabled = false;
    document.getElementById('imageInfo').innerText = `Folder: ${folderName}\nImage: ${images_path[currentIndex].name}`;
}

function displayImage(index) {
    var img = document.getElementById('currentImage');
    img.src = URL.createObjectURL(images_path[index]);

    var imageInfo = document.getElementById('imageInfo');
    imageInfo.innerText = `Folder: ${images_path[index].webkitRelativePath.split("/").slice(0, -1).join("/")}\nImage: ${images_path[index].name}`;

    if (index === images_path.length - 1) {
        imageInfo.innerText += "\n\nAll images have been shown";
    }
}

function displayQuadtreeImages(quadtreeIndex) {
    let inputImage = new Image();
    inputImage.src = quadtree.images[quadtreeIndex];
    document.getElementById('imageList').appendChild(inputImage);
  }

function handleArrowKeys(event) {
    if (event.keyCode === 37) { // Left arrow key
        currentIndex = (currentIndex === 0) ? images_path.length - 1 : currentIndex - 1;
    } else if (event.keyCode === 39) { // Right arrow key
        currentIndex = (currentIndex === images_path.length - 1) ? 0 : currentIndex + 1;
    } else if (event.keyCode === 38) { // Up arrow key
        quadtreeIndex = (quadtreeIndex === 0) ? quadtree.images.length - 1 : quadtreeIndex - 1;
    } else if (event.keyCode === 40) { // Down arrow key
        quadtreeIndex = (quadtreeIndex === quadtree.images.length - 1) ? 0 : quadtreeIndex + 1;
    }

    count = 0

    displayImage(currentIndex);
    quadtree = new Quadtree();
    let inputImage = new Image();
    inputImage.src = images_path[currentIndex];
    document.getElementById('imageList').appendChild(inputImage);
    // quadtree.checkImg(inputImage, 0, 0);
    // displayQuadtreeImages(quadtreeIndex);
}

function run(){
    displayImage(currentIndex);
    quadtree = new Quadtree();
    let inputImage = new Image();
    inputImage.src = images_path[currentIndex];
    document.getElementById('imageList').appendChild(inputImage);

    // quadtree.checkImg(inputImage, 0, 0);
    // displayQuadtreeImages(quadtreeIndex);

    document.addEventListener('keydown', handleArrowKeys);
}


document.getElementById('folderPicker').addEventListener('change', load_images_paths);
document.getElementById('startButton').addEventListener('click', run);

init() ;
