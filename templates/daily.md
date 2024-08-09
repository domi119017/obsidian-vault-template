---
tag: daily
---
# Today

<%* 
    const quoteFiles = []

    app.metadataCache.getCachedFiles().forEach(filename => { // get all filenames in the vault and iterate through all of them, calling a function for each of them
        let { tags } = app.metadataCache.getCache(filename) // get the tags in the  file w/ the given name
        tags = (tags || []).filter(t => t.tag && "#dailyquote" === t.tag) // filter out all tags that are not "#quote"
        if (tags.length > 0) { // list will contain at least one tag for the relevant notes, also filter out all notes that dont start w/ "QUOTE"
            quoteFiles.push(filename.slice(0, filename.length - 3)) // cut off last three characters from filename, otherwise the links would contain `.md` at the end
        }
    })

    const randomIndex = Math.floor(Math.random() * quoteFiles.length)

    tR += `![[${quoteFiles[randomIndex]}]]\n`
%>

## Todays Tasks
- [ ]  
## Jump back in
```dataview
LIST 
WHERE date(today) - file.mtime <= dur(3 days)
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 5
```
## ToDo
```dataview
TASK
FROM "ToDo"
WHERE !completed AND text != ""
```
## Unfinished Tasks
```dataview
TASK
FROM ""
WHERE !completed AND text != "" AND file.name != "ToDo" AND file.name != "Ideas"
```
## Ideas
```dataview
TASK
FROM "Ideas"
WHERE !completed AND text != ""
```
