//: Playground - noun: a place where people can play

import UIKit

var str = "Hello, playground"

let url = URL(string:"https://s-media-cache-ak0.pinimg.com/originals/a6/a3/91/a6a3918250ac38c9c62372e8953262ce.jpg")

do {
    let data = try Data(contentsOf: url!)
    let img = UIImage(data: data)
    let width:CGFloat = 200.0
    let newHeight = width * img!.size.height / img!.size.width
    let resized = resizeImage(image: img!, targetSize: CGSize(width: width, height: newHeight))
    let compressed = UIImageJPEGRepresentation(resized, 0.8)
    let imgComp = UIImage(data: compressed!)
    
} catch {
    print("exception")
}

func resizeImage(image: UIImage, targetSize: CGSize) -> UIImage {
    let size = image.size
    
    let widthRatio  = targetSize.width  / image.size.width
    let heightRatio = targetSize.height / image.size.height
    
    // Figure out what our orientation is, and use that to form the rectangle
    var newSize: CGSize
    if(widthRatio > heightRatio) {
        newSize = CGSize(width: size.width * heightRatio, height: size.height * heightRatio)
    } else {
        newSize = CGSize(width: size.width * widthRatio,  height: size.height * widthRatio)
    }
    
    // This is the rect that we've calculated out and this is what is actually used below
    let rect = CGRect(x: 0, y: 0, width: newSize.width, height: newSize.height)
    
    // Actually do the resizing to the rect using the ImageContext stuff
    UIGraphicsBeginImageContextWithOptions(newSize, false, 1.0)
    image.draw(in: rect)
    let newImage = UIGraphicsGetImageFromCurrentImageContext()
    UIGraphicsEndImageContext()
    
    return newImage!
}