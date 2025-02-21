<template>
  <div class="avatar-layout" :class="{ 'is-exiting': isExiting }">
    <div class="speech-bubble">
      <h1 class="bubble-title">Welcome!</h1>
      <p class="bubble-paragraph">
        {{ message }}
      </p>
      <button class="bubble-button" @click="startExitAnimation">
        Continue to Survey
      </button>
    </div>
  </div>
</template>

<script>
const SpeechSDK = window.SpeechSDK;

export default {
  data() {
    return {
      username: '',
      message: '',
      isExiting: false
    };
  },
  mounted() {
    // 从 localStorage 获取用户名
    this.username = localStorage.getItem('username') || '';
    // 从路由 query 获取后端返回的 message
    this.message = this.$route.query.message || '';

    // 启动 Avatar
    this.launchAvatarAndSpeak(this.message);
  },
  methods: {
    async launchAvatarAndSpeak(text) {
      // 1) 配置 Speech
      const speechKey = "2ySy4rYEm0BkIJDR0xXKvnUcXmJTMFs9F3w6gdTA7zEUbVR3mrvAJQQJ99BBACHYHv6XJ3w3AAAYACOGudDw";
      const speechRegion = "eastus2"; // 如果 eastus2 不可用，请改成 westus2
      const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(speechKey, speechRegion);
      speechConfig.speechSynthesisLanguage = "en-US";
      speechConfig.speechSynthesisVoiceName = "en-US-AriaNeural";

      // 2) Avatar 配置
      const avatarConfig = new SpeechSDK.AvatarConfig("lisa", "casual-sitting");

      // 3) 获取 ICE 配置
      const getIceServerConfig = async (key) => {
        // 如果 eastus2 不行，可以换 "https://westus2.tts.speech.microsoft.com/cognitiveservices/avatar/relay/token/v1"
        const endpoint = "https://eastus2.tts.speech.microsoft.com/cognitiveservices/avatar/relay/token/v1";
        const response = await fetch(endpoint, {
          method: 'GET',
          headers: { 'Ocp-Apim-Subscription-Key': key }
        });
        if (!response.ok) {
           throw new Error(`Failed to fetch ICE server info: ${response.status} - ${response.statusText}`);
        }
        const data = await response.json();
        console.log("ICE data:", data);
        return data;
      };

      const setupPeerConnection = async () => {
        const data = await getIceServerConfig(speechKey);

        const peerConnection = new RTCPeerConnection({
          iceServers: [
            {
              urls: data.Urls,    // 注意大小写
              username: data.Username,
              credential: data.Password
            }
          ]
        });

        // 监听远端 track
        peerConnection.ontrack = (event) => {
          console.log("Received track kind:", event.track.kind);
          if (event.track.kind === 'video') {
            const videoEl = document.createElement('video');
            videoEl.id = 'videoPlayer';
            videoEl.srcObject = event.streams[0];
            // 解决自动播放策略 + 全局可见样式
            videoEl.autoplay = true;
            videoEl.muted = false;       // 避免自动播放被阻止
            videoEl.playsInline = true;
            videoEl.controls = true;    // 调试时可见播放控件
            // 给视频元素一些简单样式
            videoEl.style.position = 'fixed';
            videoEl.style.zIndex = '9999';
            videoEl.style.width = '480px';
            videoEl.style.height = '360px';
            videoEl.style.bottom = '20px';
            videoEl.style.right = '20px';
            document.body.appendChild(videoEl);
          }
          if (event.track.kind === 'audio') {
            const audioEl = document.createElement('audio');
            audioEl.id = 'audioPlayer';
            audioEl.srcObject = event.streams[0];
            audioEl.autoplay = true;
            // 对音频也可能需要 muted, 但通常希望听到声音
            audioEl.controls = true; // 调试时可见
            audioEl.style.position = 'fixed';
            audioEl.style.bottom = '20px';
            audioEl.style.left = '20px';
            audioEl.style.zIndex = '9999';
            document.body.appendChild(audioEl);
          }
        };

        // 告诉浏览器我要收发一条视频和一条音频
        peerConnection.addTransceiver('video', { direction: 'sendrecv' });
        peerConnection.addTransceiver('audio', { direction: 'sendrecv' });

        return peerConnection;
      };

      // 创建 RTCPeerConnection 并启动 Avatar
      const peerConnection = await setupPeerConnection();
      const avatarSynthesizer = new SpeechSDK.AvatarSynthesizer(speechConfig, avatarConfig);

      await avatarSynthesizer.startAvatarAsync(peerConnection);
      console.log("Avatar started. WebRTC connection established.");

      // 如果需要让 Avatar 说一些话，可调用 speakTextAsync:
          avatarSynthesizer.speakTextAsync(text).then(
              (result) => {
                  if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
                      console.log("Speech and avatar synthesized to video stream.")
                  } else {
                      console.log("Unable to speak. Result ID: " + result.resultId)
                      if (result.reason === SpeechSDK.ResultReason.Canceled) {
                          let cancellationDetails = SpeechSDK.CancellationDetails.fromResult(result)
                          console.log(cancellationDetails.reason)
                          if (cancellationDetails.reason === SpeechSDK.CancellationReason.Error) {
                              console.log(cancellationDetails.errorDetails)
                          }
                      }
                  }
          }).catch((error) => {
              console.log(error)
              avatarSynthesizer.close()
          });
    },

    startExitAnimation() {
      this.isExiting = true;
      setTimeout(() => {
        this.$router.push('/questions');
      }, 600);
    }
  }
};
</script>

<style scoped>
.avatar-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #e7f8f7;
  box-sizing: border-box;
  position: relative;
  overflow: hidden; /* 避免动画中出现滚动条 */
  transition: opacity 0.6s ease;
}
.is-exiting {
  opacity: 0;
}
.speech-bubble {
  position: relative;
  width: 95%;
  max-width: 1200px;
  height: 80%;
  background: #fff;
  border-radius: 20px;
  padding: 50px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.bubble-title {
  margin-top: 0;
  font-size: 3rem;
  margin-bottom: 30px;
  color: #222;
}
.bubble-paragraph {
  font-size: 1.8rem;
  line-height: 1.8;
  margin-bottom: 32px;
  color: #333;
}
.bubble-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 20px 36px;
  font-size: 1.6rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.bubble-button:hover {
  background-color: #0056b3;
}
.doctor-image {
  position: absolute;
  bottom: 20px;
  right: 20px;
  max-width: 200px;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.doctor-image:hover {
  transform: scale(1.1);
}
/* 响应式 */
@media (max-width: 1024px) {
  .speech-bubble {
    width: 100%;
    height: auto;
    padding: 30px;
  }
  .doctor-image {
    max-width: 150px;
  }
}
</style>


