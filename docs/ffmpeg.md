### Cài đặt FFmpeg
cmd với admin quyền:
   ```bash
winget install Gyan.FFmpeg
   ```

### FFmpeg Command

1. Cắt toàn bộ frame của video:
   ```bash
   ffmpeg -i inputs/videos/video_playback_2.mp4 data/frame_%04d.jpg
   ```

2. Cắt theo FPS:
- Cắt 5 frame mỗi giây:
   ```bash
   ffmpeg -i inputs/videos/video_playback_2.mp4 -vf fps=5 data/frame_%04d.jpg
   ```
- Cắt 1 frame mỗi 5 giây:
   ```bash
    ffmpeg -i inputs/video/video_playback_2.mp4 -vf fps=0.2 data/frame_%04d.jpg
    ```

3. Cắt theo thời gian:
   ```bash
   ffmpeg -ss 10 -to 20 -i inputs/videos/video_playback_2.mp4 -vf fps=5 scale=640:640 data/frame_%04d.jpg
   ```
4. Lấy frame theo khoảng cách mỗi n frame
    ```bash
    ffmpeg -i inputs/videos/video_playback_2.mp4 -vf "select=not(mod(n\,10))" -vsync vfr data/frame_%04d.jpg
    ```