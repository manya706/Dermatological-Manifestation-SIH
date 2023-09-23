
/**
* Template Name: Medilab
* Updated: Sep 18 2023 with Bootstrap v5.3.2
* Template URL: https://bootstrapmade.com/medilab-free-medical-bootstrap-theme/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

// Start upload preview image
$(".gambar").attr(
    "src",
    "/assets/img/img-upload.jpg"
  );
  var $uploadCrop, tempFilename, rawImg, imageId;
  function readFile(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $(".upload-demo").addClass("ready");
        $("#cropImagePop").modal("show");
        rawImg = e.target.result;
      };
      reader.readAsDataURL(input.files[0]);
    } else {
      swal("Sorry - you're browser doesn't support the FileReader API");
    }
  }
  
  $uploadCrop = $("#upload-demo").croppie({
    viewport: {
      width: 500,
      height: 500
    },
    enforceBoundary: false,
    enableExif: true
  });
  $("#cropImagePop").on("shown.bs.modal", function () {
    // alert('Shown pop');
    $uploadCrop
      .croppie("bind", {
        url: rawImg
      })
      .then(function () {
        console.log("jQuery bind complete");
      });
  });
  
  $(".item-img").on("change", function () {
    imageId = $(this).data("id");
    tempFilename = $(this).val();
    $("#cancelCropBtn").data("id", imageId);
    readFile(this);
  });
  $("#cropImageBtn").on("click", function (ev) {
    $uploadCrop
      .croppie("result", {
        type: "base64",
        format: "jpeg",
        size: { width: 500, height: 500 }
      })
      .then(function (resp) {
        $("#item-img-output").attr("src", resp);
        $("#cropImagePop").modal("hide");
      });
  });
  // End upload preview image










// Handle form submission when the user clicks the "Submit" button
$("#imageSelectionForm").on("submit", function (e) {
    console.log("anujjjjjjjjjjjjjjjjj");
    alert("2");
    e.preventDefault();
  
    // Get the selected image filename
    var selectedImage = $("input[name='selectedImage']:checked").val();
  
    // Create a FormData object to store the selected image and pincode
    var formData = new FormData();
  
    // Add the selected image to the FormData
    formData.append("image_1", $(".item-img")[0].files[0]); // Uploaded image
    formData.append("image_2", selectedImage); // Selected image
  
    // Add the pincode to the FormData
    var pincode = $("#pincode").val();
    formData.append("pincode", pincode);
  
    // Send the FormData object to the server via a POST request
    $.ajax({
        url: "/your-api-endpoint-url", // Replace with your FastAPI endpoint URL
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            // Handle the response from the server
            console.log(response);
        },
        error: function (error) {
            // Handle any errors
            console.error(error);
        },
    });
  });
  
  // ... Remaining JavaScript code ...
  