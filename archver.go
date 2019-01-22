package main

// author: Artur Bakirov
// email: turkin86@mail.ru

import (
	"archive/tar"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"time"
)

func lsDir(path string) ([]os.FileInfo, error) {
	var pathDir string

	if path != "" {
		pathDir = path
	} else {
		pathDir = "."
	}

	files, err := ioutil.ReadDir(pathDir)
	if err != nil {
		log.Fatal(err)
		return nil, err
	}
	return files, nil
}

func addFilesArch(tw *tar.Writer, path string) {
	lss, _ := lsDir(path)
	for _, file := range lss {
		fpath := filepath.Join(path, file.Name())
		//fmt.Println(fpath)
		hdr, err := tar.FileInfoHeader(file, file.Name())
		if err != nil {
			log.Fatal(err)
		}
		hdr.Name = fpath
		if err := tw.WriteHeader(hdr); err != nil {
			log.Fatal(err)
		}
		if file.IsDir() {
			fmt.Println(fpath)
			addFilesArch(tw, fpath)
		} else {
			fmt.Println("\t", file.Name())
			content, err := ioutil.ReadFile(fpath)
			if err != nil {
				log.Fatal(err)
			}
			if _, err := tw.Write(content); err != nil {
				log.Fatal(err)
			}
		}
	}
}

func createTar(path string) {
	//filename extension
	fnExt := ".tar"
	//Create arhive temp file
	tfn := fmt.Sprintf("bck_*%s", fnExt)
	tf, err := ioutil.TempFile(os.TempDir(), tfn)
	if err != nil {
		log.Fatal(err)
	}
	defer tf.Close()

	// Create and add some files to the archive.
	tw := tar.NewWriter(tf)
	defer tw.Close()
	addFilesArch(tw, path)

	//Rename tmp file
	tm := time.Now()
	outFa := filepath.Join(path, fmt.Sprintf("%d%d%d%d%d%d%s", tm.Year(), tm.Month(), tm.Day(), tm.Hour(), tm.Minute(), tm.Second(), fnExt))
	if err := os.Rename(tf.Name(), outFa); err != nil {
		log.Fatal(err)
	}
}

func readTar(path string) {

	//Test open arhcive file
	htrf, err := os.OpenFile(path, os.O_RDONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	// Open and iterate through the files in the archive.
	tr := tar.NewReader(htrf)
	fmt.Println("List files:")
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break // End of archive
		}
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("\t%s\n", hdr.Name)
	}
}

func main() {
	// get list files
	srcPath := "/home/dds/"
	//	filepath.Walk(srcPath, func(file string, fi os.FileInfo, err error) error {
	//		spth := strings.TrimPrefix(strings.Replace(file, srcPath, "", -1), string(filepath.Separator))
	//        fmt.Println(file)
	//		fmt.Println(spth)
	//		return nil
	//	})

	createTar(srcPath)
}
