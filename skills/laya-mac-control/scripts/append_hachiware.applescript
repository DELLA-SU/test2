on run argv
    set savedID to item 1 of argv
    set imagePath to item 2 of argv
    set noteTitle to "Laya 하치왕왕 사진 모음"

    tell application "Notes"
        set targetNote to missing value
        if savedID is not "" then
            try
                set targetNote to note id savedID
            end try
        end if
        if targetNote is missing value then
            set targetFolder to folder "Notes" of default account
            set matches to every note of targetFolder whose name is noteTitle
            if (count of matches) > 0 then
                set targetNote to item 1 of matches
            else
                set targetNote to make new note at targetFolder with properties {name:noteTitle, body:"<div>하치와레 사진을 모읍니다.</div>"}
            end if
        end if
        set previousCount to count of attachments of targetNote
        make new attachment at end of attachments of targetNote with data (POSIX file imagePath)
        return (id of targetNote) & tab & (previousCount as text)
    end tell
end run
