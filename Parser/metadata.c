#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

const char *getFileType(const char *path){

    struct stat buf;

    if(stat(path, &buf) == -1){
        perror("stat");
        exit(EXIT_FAILURE);
    }

    int type = buf.st_mode&S_IFMT;

    if(type == S_IFBLK)
        return "block device";
    else if(type == S_IFCHR)
        return "character device";
    else if(type == S_IFDIR)
        return "directory";
    else if(type == S_IFIFO)
        return "FIFO/pipe";
    else if(type == S_IFLNK)
        return "symlink";
    else if(type == S_IFREG)
        return "regular file";
    else if(type == S_IFSOCK)
        return "socket";
    else
        return "unknown";
}

long long getLastStatusChange(const char *path){

    struct stat buf;

    if(stat(path, &buf) == -1){
        perror("stat");
        exit(EXIT_FAILURE);
    }

    return (long long)buf.st_ctime;
}

long long getLastFileAccess(const char *path){

    struct stat buf;

    if(stat(path, &buf) == -1){
        perror("stat");
        exit(EXIT_FAILURE);
    }

    return (long long)buf.st_atime;
}

long long getLastFileModification(const char *path){

    struct stat buf;

    if(stat(path, &buf) == -1){
        perror("stat");
        exit(EXIT_FAILURE);
    }

    return (long long)buf.st_mtime;
}

long long getFileSize(const char *path){

    struct stat buf;

    if(stat(path, &buf) == -1){
        perror("stat");
        exit(EXIT_FAILURE);
    }

    return (long long)buf.st_size;
}