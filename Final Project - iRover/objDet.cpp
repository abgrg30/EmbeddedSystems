#include <stdio.h>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/nonfree/nonfree.hpp"
#include <string>
#define PI 3.142
#include <unistd.h>
#include <cstdlib>


using namespace cv;
FILE *fp = fopen("camdata.txt","rw+");


bool foundObject = 0;


int rotPrev = 0;

std::string prevString="n\n";



void readme();
/** @function main */
int main( int argc, char** argv )
{
  if( argc != 1 )
  { readme(); return -1; }


#ifdef STILL
  Mat img_object = imread( "env.jpg", CV_LOAD_IMAGE_COLOR );
#else
  Mat img_object = imread( "box.png", CV_LOAD_IMAGE_GRAYSCALE );
  Mat img_o = imread( "box.png", CV_LOAD_IMAGE_COLOR);
#endif
  int minHessian = 100;
  SurfFeatureDetector detector( minHessian );
  namedWindow("Good Matches & Object detection",WINDOW_NORMAL);
  
  


 
  std::vector<KeyPoint> keypoints_object;
  detector.detect( img_object, keypoints_object);
  SurfDescriptorExtractor extractor;
  Mat descriptors_object;
  extractor.compute(img_object, keypoints_object, descriptors_object);
  double max_dist = 0; double min_dist = 100;
  
  //VideoCapture cap(1); 
#ifndef STILL
  VideoCapture cap("fifo"); 
#endif
  rotPrev = 90;
  int rotation;	
	
  int frCount = 0; 	
	
  while(char((waitKey(1))!='q'))
 {
#ifdef STILL
  Mat img_scene = imread( "scene.jpg", CV_LOAD_IMAGE_COLOR );
#else
  Mat img_scene;	
  cap>>img_scene; 
 if(frCount!=9)
   {
        frCount++;		
	continue; 
   }
   else 
       frCount=0;		

#endif
  if( !img_object.data || !img_scene.data )
  { std::cout<< " --(!) Error reading images " << std::endl; return -1; }
  
  



  //-- Step 1: Detect the keypoints using SURF Detector

  std::vector<KeyPoint> keypoints_scene;
  detector.detect( img_scene, keypoints_scene );

  //-- Step 2: Calculate descriptors (feature vectors)

  Mat  descriptors_scene;

  extractor.compute( img_scene, keypoints_scene, descriptors_scene );

  //-- Step 3: Matching descriptor vectors using FLANN matcher
  FlannBasedMatcher matcher;

 	

#if 1
  std::vector< DMatch > matches;
  matcher.match( descriptors_object, descriptors_scene, matches );


  //-- Quick calculation of max and min distances between keypoints
  for( int i = 0; i < descriptors_object.rows; i++ )
  { double dist = matches[i].distance;
    if( dist < min_dist ) min_dist = dist;
    if( dist > max_dist ) max_dist = dist;
  }

  //printf("-- Max dist : %f \n", max_dist );
  //printf("-- Min dist : %f \n", min_dist );

  //-- Draw only "good" matches (i.e. whose distance is less than 3*min_dist )
  std::vector< DMatch > good_matches;

  for( int i = 0; i < descriptors_object.rows; i++ )
  { if( matches[i].distance < 2*min_dist )
     { good_matches.push_back( matches[i]); }
  }

#else
 vector<Mat> train_desc_collection(1, descriptors_object);
 matcher.add(train_desc_collection);
 matcher.train();

 

 vector<vector<DMatch> > matches;
 matcher.knnMatch(descriptors_scene,matches,2);
// filter for good matches according to Lowe's algorithm



 std::cerr<<"Matches size = "<<matches.size()<<"\n";

 vector<DMatch> good_matches;
 for(int i = 0; i < matches.size(); i++) {
   if(matches[i][0].distance < 0.6* matches[i][1].distance)
    good_matches.push_back(matches[i][0]);
}
 
 

#endif


  Mat img_matches;
  drawMatches( img_object, keypoints_object, img_scene, keypoints_scene,
               good_matches, img_matches, Scalar::all(-1), Scalar::all(-1),
               vector<char>(), DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS );

  //-- Localize the object
  std::vector<Point2f> obj;
  std::vector<Point2f> scene;

  for( int i = 0; i < good_matches.size(); i++ )
  {
    //-- Get the keypoints from the good matches
    obj.push_back( keypoints_object[ good_matches[i].queryIdx ].pt );
    scene.push_back( keypoints_scene[ good_matches[i].trainIdx ].pt );
  }


  if((obj.size()>=4)&&(scene.size()>=4))
   { 
      Mat H = findHomography( obj, scene, CV_RANSAC );

  //-- Get the corners from the image_1 ( the object to be "detected" )
      std::vector<Point2f> obj_corners(4);
      obj_corners[0] = cvPoint(0,0); obj_corners[1] = cvPoint( img_object.cols, 0 );
      obj_corners[2] = cvPoint( img_object.cols, img_object.rows ); obj_corners[3] = cvPoint( 0, img_object.rows );
      std::vector<Point2f> scene_corners(4);

      perspectiveTransform( obj_corners, scene_corners, H);
      //std::cerr<<scene_corners.size(); 	
      
  


      //-- Draw lines between the corners (the mapped object in the scene - image_2 )
      line( img_matches, scene_corners[0] + Point2f( img_object.cols, 0), scene_corners[1] + Point2f( img_object.cols, 0), Scalar(0, 255, 0), 4 );
      line( img_matches, scene_corners[1] + Point2f( img_object.cols, 0), scene_corners[2] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );
      line( img_matches, scene_corners[2] + Point2f( img_object.cols, 0), scene_corners[3] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );
      line( img_matches, scene_corners[3] + Point2f( img_object.cols, 0), scene_corners[0] + Point2f( img_object.cols, 0), Scalar( 0, 255, 0), 4 );

      Point2f diff1 = scene_corners[1]-scene_corners[0];
      Point2f diff2 = scene_corners[3]-scene_corners[0];

      float x1,x2,x3,x4;
      float y1,y2,y3,y4;
       
       x1 = scene_corners[0].x;y1 = scene_corners[0].y;	
       x2 = scene_corners[1].x;y2 = scene_corners[1].y;	
       x3 = scene_corners[2].x;y3 = scene_corners[2].y;	
       x4 = scene_corners[3].x;y4 = scene_corners[3].y;	
		


      int cmp1 = (x1<321)&(x2<321)&(x3<321)&(x4<320);			
      int cmp3 = (x1>0)&(x2>0)&(x3>0)&(x4>0);			
		
      int cmpF = cmp1 & cmp3 ;  
		
	
       
      float d1 = sqrt((diff1.x)*(diff1.x) + (diff1.y)*(diff1.y)); 
      float d2 = sqrt((diff2.x)*(diff2.x) + (diff2.y)*(diff2.y)); 

	
//	std::cerr << d1<<d2<<std::endl;

      
      if((d1<15)||(d2<15))    
       {
	std::string rotString = "n\n";
	std::cerr<<rotString;
	prevString = rotString;

       }


      else if(((d1>120)&&(d1<250))&&(d2>120)&&((d2<250))) 
      {

      	double obj_cx = (scene_corners[0].x+scene_corners[1].x)/2; 	
      	double obj_cy = (scene_corners[0].y+scene_corners[3].y)/2;
	
        		

      	double scene_orig_x = (img_scene.cols)/2;
      	double scene_orig_y = (img_scene.rows);		
     
      	double yDis = -obj_cy + scene_orig_y;
        double xDis = obj_cx  - scene_orig_x;
	 

	rotation =  atan2(yDis,xDis)*180/PI-90;

	//if(rotation)	

	rotPrev = rotation;
	std::stringstream convert;
	convert<<rotation;
//	std::cerr<<d1<<"\t"<<d2<<" ";
	std::string  rotString = convert.str();
	std::string  res = rotString;		
	std::cerr << res<<std::endl;

 	prevString = rotString;	
	



      }
      
         	
      
        //std::cout<<"\nHeading = "<<rotation<<" degrees\n";	 	

      //-- Show detected matches
      imshow( "Good Matches & Object detection", img_matches );
   	
    } 	
    else
       {
	
	rotation = rotPrev;
	std::string rotString = "n\n";
	std::cerr<<rotString;
/*	
	if(prevString=="n\n")
	
	{	
	  std::cerr << prevString;
	  continue;
        }

       else
       {	
	   std::string res; 	
	   if(prevString=="-2\n")	
	   	 res = "2\n";
	   else
		 res = "-2\n";				
	  prevString = res;	
	  std::cerr<<res;
       }
*/

   }//
  }
  return 0;
  }

  /** @function readme */
  void readme()
  { std::cout << " Usage: ./SURF_descriptor <img1> <img2>" << std::endl; }
