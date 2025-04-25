# YT-DLP Helper Script

> Inspired by @ThioJoe

A user-friendly PowerShell script for easy video downloading using yt-dlp.

## Quick Start

1. Ensure [yt-dlp](https://github.com/yt-dlp/yt-dlp) is installed and in your system PATH.
2. Clone this repository or download the `yt-dlp-helper.ps1` script.
3. Run the script in PowerShell:

    ```powershell
    .\yt-dlp-helper.ps1
    ```

4. Follow the prompts to download videos or playlists.

### Advanced Usage

```powershell
.\yt-dlp-helper.ps1 -exe "yt-dlp.exe" -desktop -options "--no-mtime --add-metadata --extract-audio"
```

## Detailed Guide

### Prerequisites

1. **Install yt-dlp**: This script requires the [yt-dlp](https://github.com/yt-dlp/yt-dlp) program. Follow the installation instructions on their GitHub page.
2. **Add yt-dlp to PATH**: Ensure that yt-dlp is accessible from any location in your command prompt or PowerShell.

### Running the Script

1. Open PowerShell.
2. Navigate to the directory containing the script.
3. Run the script by typing:

    ```powershell
    .\yt-dlp-helper.ps1
    ```

### Using the Script

1. **Enter URL**: When prompted, paste the URL of the video or playlist you want to download.

2. **Choose Download Option**:
   - Option 1: Automatic download (best quality)
   - Option 2: Best quality single file
   - Option 3: Highest quality audio and video, combined
   - Option 4: Choose custom video and audio formats
   - Option 5: Download only audio or video
   - Option 6: Download a specific single file
   - Option 7: Update yt-dlp

3. **Format Selection**: For options 4, 5, and 6, you'll need to choose specific format codes. The script will display available formats for you to choose from.

4. **Confirmation**: The script will show you the selected format and ask for confirmation before downloading.

5. **Download**: Once confirmed, the download will begin. Files are saved in the current directory by default.

### Additional Features

- **Desktop Output**: Use the `-desktop` switch to save files to a 'Outputs' folder on your desktop.
- **Custom Options**: Use the `-options` parameter to pass additional options to yt-dlp.
- **Debug Mode**: Use the `-debug` switch to display additional information for troubleshooting.

### Supported Sites

This script can download from various websites supported by yt-dlp. For a full list, visit [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Troubleshooting

- If you encounter issues, ensure yt-dlp is up to date by running the script with option 7.
- Check that yt-dlp is correctly added to your system PATH.
- For more detailed error information, run the script with the `-debug` switch.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit issues or pull requests on the GitHub repository.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments

- This script is a wrapper for [yt-dlp](https://github.com/yt-dlp/yt-dlp), an excellent fork of youtube-dl.
- Author: Shane Holloman
- GitHub: <https://github.com/shaneholloman>
