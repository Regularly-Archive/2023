
<template>
    <div class="hello">
        <video controls width="480">
            <source src="http://localhost:5137/api/Files/download?fileName=flower.webm" type="video/webm">

            <source src="http://localhost:5137/api/Files/download?fileName=flower.mp4" type="video/mp4">

            点击下载视频
            <a href="http://localhost:5137/api/Files/download?fileName=flower.webm">.webm</a>
            或者
            <a href="http://localhost:5137/api/Files/download?fileName=flower.mp4">.mp4</a>
        </video>
    </div>
</template>
  
<script>
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>