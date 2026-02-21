import os
from google.colab import drive
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# 1. Google Drive 마운트 (Mount Google Drive)
print("Mounting Google Drive...")
drive.mount('/content/drive')

def generate_youtube_video(audio_path, image_folder, output_path):
    # 2. 출력 디렉토리 생성 확인
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 3. 오디오 로드
    print(f"Loading audio: {audio_path}")
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    # 4. 이미지 로드
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
                   if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
    num_images = len(image_files)
    
    if num_images == 0:
        print("Error: No images found in the folder.")
        return

    # 5. 계산: 이미지당 재생 시간 (Duration per Image)
    duration_per_image = total_duration / num_images
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Number of Images: {num_images}")
    print(f"Duration per Image: {duration_per_image:.2f} seconds")

    # 6. 클립 생성 및 교차 페이드(Crossfade) 적용
    clips = []
    fade_duration = 0.5  # 교차 페이드 시간 (초)
    
    for img_path in image_files:
        # 페이드 시간을 고려하여 클립 길이를 약간 더 길게 설정
        clip = ImageClip(img_path).set_duration(duration_per_image + fade_duration)
        clip = clip.crossfadein(fade_duration)
        clips.append(clip)

    # 7. 클립 합성 및 오디오 설정
    print("Synthesizing video with Crossfade...")
    final_video = concatenate_videoclips(clips, method="compose", padding=-fade_duration)
    final_video = final_video.set_audio(audio).set_duration(total_duration)

    # 8. 렌더링 및 저장
    print(f"Starting Rendering to: {output_path}")
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    print("\n" + "="*50)
    print("✨ Rendering Complete!")
    print(f"📁 File saved in: {output_path}")
    print(f"🔗 Access your folder here: https://drive.google.com/drive/folders/1TMb9lwMPBWjoHUSvlaVIhvQWxWJ-s8Tk")
    print("="*50)

# --- 설정 (Configuration) ---
# 구글 드라이브 구조에 맞게 경로를 수정하세요.
AUDIO_PATH = "/content/drive/MyDrive/YouTube_Project/assets/background_audio.mp3"
IMAGE_FOLDER = "/content/drive/MyDrive/YouTube_Project/assets/images/"
OUTPUT_PATH = "/content/drive/MyDrive/YouTube_Project/output/final_video.mp4"

if __name__ == "__main__":
    # 파일 및 폴더 존재 여부 확인 후 실행
    if os.path.exists(AUDIO_PATH) and os.path.exists(IMAGE_FOLDER):
        generate_youtube_video(AUDIO_PATH, IMAGE_FOLDER, OUTPUT_PATH)
    else:
        print("Error: 자산이 지정된 드라이브 경로에 존재하는지 확인하십시오.")
        print(f"오디오 파일 누락: {not os.path.exists(AUDIO_PATH)}")
        print(f"이미지 폴더 누락: {not os.path.exists(IMAGE_FOLDER)}")
