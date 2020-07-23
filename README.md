Simple script for renaming TV show files into a standard format.

Here, we use Kodi's suggestion for describing the season and episode.
For example, for season 2, episode 7, the video file should contain "S02E07".

This script is currently able to match and fix the following formats:
   * 207
   * 0207
   * 2.07
   * 02.07
   * s02e07
   * s2e7
  
Please be careful when passing movie files, as the year may be incorrectly
interpreted. "Movie.2010.DVDRip.avi" could become "Movie.S20E10.DVDRip.avi".

Optional arguments:

   * [path] - where the script should run (defaults to current dir)
   * -p|--preview - does not rename, just prints the expected outcome
   * -f|--force - does not ask for confirmation (potentially destructive)
   * -t|--title - capitalize the first letter of each segment
   * -l|--lower|--lowercase - uncapitalize whole filename
   * -u|--upper|--uppercase - capitalize whole filename
