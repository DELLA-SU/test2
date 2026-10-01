on run argv
    tell application "Notes"
        set targetNote to note id (item 1 of argv)
        set targetName to item 2 of argv
        set matches to every attachment of targetNote whose name is targetName
        return ((count of attachments of targetNote) as text) & tab & ((count of matches) as text)
    end tell
end run
