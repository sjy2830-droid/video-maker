import os
from google.colab import drive
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# 1. Google Drive 마운트
print("Mounting Google Drive...")
drive.mount('/content/drive')

def generate_youtube_video(audio_path, image_folder, output_path):
    # 2. 출력 디렉토리 확인
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 3. 오디오/이미지 로드 및 영상 제작
    audio = AudioFileClip(audio_path)
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
    
    duration_per_image = audio.duration / len(image_files)
    clips = [ImageClip(img).set_duration(duration_per_image).crossfadein(0.5) for img in image_files]
    
    final_video = concatenate_videoclips(clips, method="compose", padding=-0.5)
    final_video = final_video.set_audio(audio).set_duration(audio.duration)

    # 4. 저장 및 링크 출력
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    print("\n✨ 렌더링 완료!")
    print(f"🔗 폴더 링크: https://drive.google.com/drive/folders/1TMb9lwMPBWjoHUSvlaVIhvQWxWJ-s8Tk")

# 설정 경로
AUDIO_PATH = "/content/drive/MyDrive/YouTube_Project/assets/background_audio.mp3"
IMAGE_FOLDER = "/content/drive/MyDrive/YouTube_Project/assets/images/"
OUTPUT_PATH = "/content/drive/MyDrive/YouTube_Project/output/final_video.mp4"

if __name__ == "__main__":
    generate_youtube_video(AUDIO_PATH, IMAGE_FOLDER, OUTPUT_PATH)
