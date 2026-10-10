use framework "AppKit"
use scripting additions

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
        set targetID to id of targetNote
        show targetNote
        activate
        set selectedNotes to {}
        repeat 100 times
            set selectedNotes to selection
            if (count of selectedNotes) is 1 then
                if (id of item 1 of selectedNotes) is targetID then exit repeat
            end if
            delay 0.1
        end repeat
        if (count of selectedNotes) is not 1 then error "전용 메모 선택을 확인하지 못했습니다."
        if (id of item 1 of selectedNotes) is not targetID then error "다른 메모가 선택되어 사진 추가를 중단했습니다."
    end tell

    tell application "System Events"
        tell process "Notes"
            set frontmost to true
            set targetWindow to missing value
            repeat 100 times
                if frontmost then
                    repeat with candidateWindow in windows
                        try
                            if exists text area 1 of scroll area 2 of splitter group 1 of candidateWindow then
                                set targetWindow to contents of candidateWindow
                                exit repeat
                            end if
                        end try
                    end repeat
                end if
                if targetWindow is not missing value then exit repeat
                delay 0.1
            end repeat
            if targetWindow is missing value then error "메모 편집창을 찾지 못했습니다. 메모 창을 연 뒤 다시 실행해 주세요."
            set focused of text area 1 of scroll area 2 of splitter group 1 of targetWindow to true
            key code 126 using {command down}
            key code 125
        end tell
    end tell

    -- Paste the file itself. This inserts a named attachment without an Open dialog.
    -- Keep all clipboard formats and restore them unless the user copied something new.
    set pasteboard to current application's NSPasteboard's generalPasteboard()
    set savedItems to current application's NSMutableArray's array()
    repeat with oldItem in pasteboard's pasteboardItems()
        set copiedItem to current application's NSPasteboardItem's alloc()'s init()
        repeat with itemType in oldItem's types()
            set oldData to oldItem's dataForType:itemType
            if oldData is not missing value then copiedItem's setData:oldData forType:itemType
        end repeat
        savedItems's addObject:copiedItem
    end repeat
    pasteboard's clearContents()
    set fileURL to current application's NSURL's fileURLWithPath:imagePath
    set wroteFile to pasteboard's writeObjects:{fileURL}
    set pasteVersion to pasteboard's changeCount() as integer
    try
        if not (wroteFile as boolean) then error "사진 첨부 파일을 준비하지 못했습니다."
        tell application "Notes"
            set selectedNotes to selection
            if (count of selectedNotes) is not 1 then error "전용 메모 선택이 바뀌었습니다."
            if (id of item 1 of selectedNotes) is not targetID then error "다른 메모가 선택되어 사진 추가를 중단했습니다."
        end tell
        tell application "System Events" to tell process "Notes"
            if not frontmost then error "메모 앱이 앞에 있지 않아 사진 추가를 중단했습니다."
            key code 9 using {command down}
        end tell
        set attached to false
        repeat 200 times
            tell application "Notes"
                if (count of attachments of (note id targetID)) > previousCount then
                    set attached to true
                    exit repeat
                end if
            end tell
            delay 0.1
        end repeat
        if not attached then error "메모에 사진 첨부가 완료됐는지 확인하지 못했습니다."
    on error errorMessage number errorNumber
        my restoreClipboard(pasteboard, savedItems, pasteVersion)
        error errorMessage number errorNumber
    end try
    my restoreClipboard(pasteboard, savedItems, pasteVersion)

    return targetID & tab & (previousCount as text)
end run


on restoreClipboard(pasteboard, savedItems, pasteVersion)
    if (pasteboard's changeCount() as integer) is pasteVersion then
        pasteboard's clearContents()
        if (savedItems's |count|() as integer) > 0 then pasteboard's writeObjects:savedItems
    end if
end restoreClipboard
