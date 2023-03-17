<template>
    <TheHeader/>
    <span v-if="!imageData">
        <section id="form-container" v-if="!loading">
            <form id="credentials-form" @submit.prevent="getDataImage">
                <div class="title">Upload images</div>

                <div class="input-container">
                    <label for="files">Images:  </label>
                    <input @change="handleFiles" id="files" type="file" multiple required/>
                </div>
                
                <p>Offer have exactly 3 images, so upload 3 images on 1 offer</p>
                <p>Payment, location and delivery settings are taken from the last offer </p>
                <p>Description is predefined - <a href="https://ik.imagekit.io/ybcdqxxka/description.png?ik-sdk-version=javascript-1.4.3&updatedAt=1678128953875" target="_blank">preview</a></p>
                <button type="submit" class="blue-button">Send images</button>
            </form>
        </section>

        <div id="loading" v-if="loading">
            <img src="../assets/spinner.gif" alt="loading">
        </div>
    </span>

    <TheListingData v-if="imageData" :imageData="imageData"/>
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import TheListingData from '@/components/TheListingData.vue'
    import VueCookies from 'vue-cookies'
    import axios from 'axios'

    export default {
        
        data(){
            return{
                data: [],
                imageData: "",
                loading: false,
            }
        },

        methods:{
            handleFiles(event) {
                // Get an array of the selected files and sort them by name
                const files = Array.from(event.target.files)
                files.sort((a, b) => a.name.localeCompare(b.name))

                let loadedCount = 0
                // Loop through the files and read each one as a data URL
                for (let i = 0; i < files.length; i++) {
                    const reader = new FileReader()
                    reader.readAsDataURL(files[i])
                    reader.onload = () => {
                        this.data[i] = reader.result
                        loadedCount++
                        if (loadedCount === files.length) {
                            // All files have been loaded, sort the data array
                            this.data.sort((a, b) => files.findIndex(file => file.name === a.split(',')[0].split(';')[1]) - files.findIndex(file => file.name === b.split(',')[0].split(';')[1]))
                        }
                    }
                }
            },

            async getDataImage() {
                this.loading = true
                try 
                {
                    await axios.post('http://127.0.0.1:8000/read-image', {images: this.data}, {headers: {'Content-Type': 'application/json'}})
                    this.imageData = await axios.get('http://127.0.0.1:8000/data-image')
                } 
                catch (error) 
                {
                    alert('Upload failed.')
                }
                this.loading = false
            },
        },

        components:{
            TheHeader,
            TheListingData,
            VueCookies 
        }
    }
</script>

<style lang="scss" scoped>
    #form-container {
        display: flex;
        justify-content: center;
        width: 100%;

        #credentials-form {
            display: flex;
            flex-direction: column;
            margin-top: 50px;
            border-radius: 25px;
            padding: 20px;
            background-color: rgb(34, 36, 36);
            width: 50%;
            gap: 20px;

            .title {
                font-size: 36px;
                font-weight: 600;
                margin-top: 15px;
            }

            .input-container {
                height: 50px;
                position: relative;
                width: 100%;
            }
        }

        p{
            a{
                opacity: 0.8;
            }

            a:hover{
                opacity: 1;
            }
        }
    }

@media only screen and (max-width: 750px) {
    #credentials-form{
        min-width: 500px;
    }
}

@media only screen and (max-width: 500px) {
    #form-container{
        width: 500px;
        
        #credentials-form{
            min-width: 350px;
        }
    }
}

    
</style>