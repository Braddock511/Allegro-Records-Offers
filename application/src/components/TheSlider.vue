<template>
    <span v-if="!loading">
        <vue-easy-lightbox
            scrollEnabled
            escEnabled
            moveEnabled
            :visible="visible"
            :imgs="images[currentIndex]"
            :zoomScale="1.5"
            @hide="visible = false">
        </vue-easy-lightbox>
        <div class="slider">
        <div class="arrow-left" @click="prevImage" style="left: 10px;">&#8249;</div>
        <div class="image-container">
            <img :src="images[currentIndex]" alt="Slider Image" @click="visible = true">
        </div>
        <div class="arrow-right" @click="nextImage" style="right: 10px;">&#8250;</div>
        </div>
    </span>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
</template>
  
<script>
    import VueEasyLightbox from 'vue-easy-lightbox'
    export default {
        data() {
            return {
                currentIndex: 0,
                visible: false,
                loading: false
            }
        },
        methods: {
            prevImage() {
                if (this.currentIndex > 0) {
                    this.currentIndex -= 1
                } else {
                    this.currentIndex = this.images.length - 1
                }
            },
            nextImage() {
                if (this.currentIndex < this.images.length - 1) {
                    this.currentIndex += 1
                } else {
                    this.currentIndex = 0
                }
            }
        },
        mounted(){
            this.loading = true
            const images = this.images
            const promises = images.map(imgSrc => {
                return new Promise(resolve => {
                    const img = new Image()
                    img.onload = resolve
                    img.src = imgSrc
                })
            })
            Promise.all(promises).then(() => {
                this.loading = false
            })
        },
        props: {
            images: {
                type: Array,
                required: true
            }
        },
        components: {
            VueEasyLightbox
        }
    }
</script>

<style lang="scss" scoped>
.slider {
    position: relative;
    display: flex;
    align-items: center;
    width: 750px;
    .arrow-left, .arrow-right {
        position: absolute;
        z-index: 3;
        top: 50%;
        transform: translateY(-50%);
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: rgba(0, 0, 0, 0.5);
        font-size: 24px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .image-container {
        flex: 1;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;   
        img {
            max-width: 100%;
            height: 560px;
            object-fit: contain;
            cursor: pointer;
            &:hover{
                opacity: 0.9;
            }
        }
    }
}
@media only screen and (max-width: 820px) {
    .slider{
        width: 500px;
    }
}
</style>