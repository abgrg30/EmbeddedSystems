import java.awt.*;       // Using AWT containers and components
import java.awt.event.*; // Using AWT events and listener interfaces
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.*;
import java.lang.System;
import javax.swing.*;    // Using Swing components and containers
import java.net.*;

//A Swing GUI application inherits from top-level container javax.swing.JFrame
public class JavaClient extends JFrame
{
	private JPanel p;
	private JTextField d;
	private JTextField mx;
	private JTextField my;
	private JTextField mz;
	private JTextField ang;
	private JTextField cam;
	
	private int camcount;
	
	public Boolean ready;
	private Socket client;
	private PrintWriter out;
	private BufferedReader in;
	private BufferedReader stdIn;
	
	public JavaClient()
	{
		ready = false;
		camcount = 0;
		
		int c = 1000;
		int r = 1000;
		int x = 0;
		int y = 0;
		int rbutton = 80;
		int cbutton = 160;
		int buttonpos = c-2*cbutton;
		
	    // Retrieve the content-pane of the top-level container JFrame
	    // All operations done on the content-pane
	    Container pane = getContentPane();
	    
	    p = new JPanel();
	    p.setBounds(x, y, r, c);
	    p.setBackground(Color.BLUE);
	    p.setLayout(null);
	    pane.add(p);
	      
	    JButton up = new JButton("forward");
	    JButton left = new JButton("left");
	    JButton stop = new JButton("stop");
	    JButton right = new JButton("right");
	    JButton down = new JButton("down");
	    JButton start = new JButton("start");
	    JButton end = new JButton("end");
	    
	    JButton cameraleft = new JButton("camera left");
	    JButton cameraright = new JButton("camera right");
	    
	    JButton distance = new JButton(" Obstacle Distance");
	    JButton gps = new JButton("Get Coordinates(GPS)");
	    JButton scan = new JButton("Scan & Approach");
	    
	    d = new JTextField("0 cm", 10);
	    mx = new JTextField("x :0", 10);
	    my = new JTextField("y :0", 10);
	    mz = new JTextField("z :0", 10);
	    ang = new JTextField("deg :0", 10);
	    cam = new JTextField("dir count :0", 10);
	    
	    Font font1 = new Font("SansSerif", Font.BOLD, 20);
	    JTextField label = new JTextField("iROVER MISSION CONTROL", 10);
	    label.setFont(font1);
	    label.setHorizontalAlignment(JTextField.CENTER);
	    cam.setHorizontalAlignment(JTextField.CENTER);
	    d.setHorizontalAlignment(JTextField.CENTER);
	    mx.setHorizontalAlignment(JTextField.CENTER);
	    my.setHorizontalAlignment(JTextField.CENTER);
	    mz.setHorizontalAlignment(JTextField.CENTER);
	    ang.setHorizontalAlignment(JTextField.CENTER);
	    
	    d.setEditable(false);
	    mx.setEditable(false);
	    my.setEditable(false);
	    mz.setEditable(false);
	    ang.setEditable(false);
	    label.setEditable(false);
	    cam.setEditable(false);
	    
	    up.setBounds(buttonpos, r-4*rbutton, cbutton, rbutton);
	    stop.setBounds(buttonpos, r-3*rbutton, cbutton, rbutton);
	    left.setBounds(buttonpos-cbutton, r-3*rbutton, cbutton, rbutton);
	    right.setBounds(buttonpos+cbutton, r-3*rbutton, cbutton, rbutton);
	    down.setBounds(buttonpos, r-2*rbutton, cbutton, rbutton);	    
	    
	    start.setBounds(10, r-4*rbutton, cbutton, rbutton);
	    end.setBounds(cbutton + 30, r-4*rbutton, cbutton, rbutton);
	    
	    cameraleft.setBounds(10, r-3*rbutton + 20, cbutton, rbutton);
	    cameraright.setBounds(cbutton + 30, r-3*rbutton + 20, cbutton, rbutton);
	    cam.setBounds(10, r-2*rbutton + 30, 2*cbutton+20, rbutton);
	    
	    rbutton = 120;
	    
	    distance.setBounds(c-2*cbutton -30, rbutton, cbutton, rbutton);
	    gps.setBounds(c-2*cbutton -30, 2*rbutton, cbutton, rbutton);
	    scan.setBounds(c-cbutton -30, 3*rbutton+rbutton/3, cbutton, rbutton);	    
	    
	    d.setBounds(c-cbutton -30, rbutton, cbutton, rbutton);
	    mx.setBounds(c-cbutton -30, 2*rbutton, cbutton, rbutton/4);
	    my.setBounds(c-cbutton -30, 2*rbutton+rbutton/4, cbutton, rbutton/4);
	    mz.setBounds(c-cbutton -30, 2*rbutton+2*rbutton/4, cbutton, rbutton/4);
	    ang.setBounds(c-cbutton -30, 2*rbutton+3*rbutton/4, cbutton, rbutton/4);
	    label.setBounds(10, 10, 500, 500);	    
	    
	    p.add(up);
	    p.add(left);
	    p.add(stop);	      
	    p.add(right);
	    p.add(down);
	    p.add(start);
	    p.add(end);
	    p.add(cameraleft);
	    p.add(cameraright);
	    p.add(distance);
	    p.add(gps);
	    p.add(scan);  
	    
	    p.add(d);
	    p.add(mx);
	    p.add(my);
	    p.add(mz);
	    p.add(ang);
	    p.add(label);
	    p.add(cam);
	    
	    scan.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("11");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    start.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("0");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    up.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("1");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    down.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("2");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    right.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("3");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    left.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{	    		
	        		out.println("4");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    cameraleft.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("5");
	        		camcount--;
	        		cam.setText("dir count :"+camcount);
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    cameraright.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{
	        		out.println("6");
	        		camcount++;
	        		cam.setText("dir count :"+camcount);
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    stop.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{		    		
	        		out.println("9");
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    distance.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{		    		
	        		out.println("7");
	        		
	        		try {
						d.setText(in.readLine()+" cm");
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    gps.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{		    		
	        		out.println("8");
	        		String s;
					try 
					{
						s = in.readLine();
		        		int num = 0;
		        		int start=0;
		        		String temp;
		        		
		        		for(int i=0;i<s.length();i++)
		        		{
		        			if(s.charAt(i) == ',')
		        			{
	        					num++;
	        					temp = s.substring(start, i);
	        					start = i+1;
	        					
		        				if(num == 1)
		        				{
		        					mx.setText("x : "+temp);
		        				}
		        				else if(num == 2)
		        				{
		        					my.setText("y : "+temp);
		        				}
		        				else if(num == 3)
		        				{
		        					mz.setText("z : "+temp);
		        				}
		        				else if(num == 4)
		        				{
		        					ang.setText("deg : "+temp);
		        				}
		        			}
		        		}
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    end.addMouseListener(new MouseListener() 
	    {
	        public void mouseClicked(MouseEvent e) 
	        {
	        	if(checkcondition())
	        	{		    		
	        		out.println("10");
					System.out.println("Terminating Code");
					
					try 
					{
						out.close();
						in.close();
						stdIn.close();
						client.close();
					} 
					catch (IOException e1) 
					{
						System.out.println("\n IO Exception \n");
						e1.printStackTrace();
					}

	        	}
	        }
	        
	        public void mouseEntered(MouseEvent e) {}
	        public void mouseExited(MouseEvent e) {}
	        public void mousePressed(MouseEvent e) {}
	        public void mouseReleased(MouseEvent e) {}
	    });
	    
	    //p.setFocusable(true);
	    
        p.addFocusListener(new FocusAdapter() 
        {
            public void focusLost(FocusEvent ev) 
            {
              p.requestFocus();
            }
        });
        
	    p.addKeyListener(new KeyAdapter()
	    {
	        public void keyTyped(KeyEvent e){}
	        
	        public void keyPressed(KeyEvent e)
	        {
	        	int keyCode = e.getKeyCode();
	        	System.out.println("key pressed, keycode : " + keyCode + "");
	        	
	            switch(keyCode)
	            {
	            	case KeyEvent.VK_UP:
	            	{	            	
	            		keyCode = 1;
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_DOWN:
	            	{	            	
	            		keyCode = 2;
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_RIGHT:
	            	{	            	
	            		keyCode = 3;
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_LEFT:
	            	{	            	
	            		keyCode = 4;
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_HOME:
	            	{	            	
	            		keyCode = 5;
	            		camcount--;
	            		cam.setText("dir count :"+camcount);
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_END:
	            	{	            	
	            		keyCode = 6;
	            		camcount++;
	            		cam.setText("dir count :"+camcount);
	            	}
	            	break;
	            	
	            	case KeyEvent.VK_CONTROL:
	            	{	            	
	            		keyCode = 7;
	            	}
	            	break;
	            	
	            	default:
	            		break;
	            }
	            
	            //if (up.getModel().isPressed()) 
	            {
		        	if(checkcondition())
		        	{
		        		out.println(keyCode+"");
		        	}
	            } 
	            //else 
	            {
	                // just in case it can happen that the button is released on
	                // a key press action (maybe another controls key listener...)
	            }
	        }

	        public void keyReleased(KeyEvent e){}
	    });
	      
	    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);  // Exit program if close-window button clicked
	    setTitle("IROBOT GUI"); // "this" JFrame sets title
	    setSize(r, c);         // "this" JFrame sets initial size
	    setResizable(false);
	    setVisible(true);          // "this" JFrame shows
	    
	    p.requestFocus();
	    
	    ready = true;
	}
	
	public Boolean checkcondition()
	{
	    if(client.isConnected()) 
	    {
	    	if(client.isClosed() == false)
	    	{
	    		return true;
	    	}
	    }
	    
	    return false;
	}
	
	public void init_socket()
	{
		try 
		{
			client = new Socket("192.168.43.2", 5000);
			//client = new Socket("192.168.7.2", 12000);
		    out = new PrintWriter(client.getOutputStream(), true);
			//DataOutputStream out = new DataOutputStream(client.getOutputStream());
			//DataInputStream in = new DataInputStream(client.getInputStream());
			//DataInputStream stdIn = new DataInputStream(System.in);
		    in = new BufferedReader(new InputStreamReader(client.getInputStream()));
		    stdIn = new BufferedReader(new InputStreamReader(System.in));
		} 
		catch (UnknownHostException e) 
		{
			System.out.println("\n IP address of the host could not be determined \n");
			e.printStackTrace();
		} 
		catch (IOException e) 
		{
			System.out.println("\n IO Exception \n");
			e.printStackTrace();
		}
		catch (SecurityException e) 
		{
			System.out.println("\n security manager exists and its checkConnect method doesn't allow the operation \n");
			e.printStackTrace();
		}
		catch (IllegalArgumentException e) 
		{
			System.out.println("\n the port parameter is outside the specified range of valid port values, which is between 0 and 65535, inclusive \n");
			e.printStackTrace();
		}
	}

	public static void main(String[] args) 
	{
		// Run the GUI construction in the Event-Dispatching thread for thread-safety
		SwingUtilities.invokeLater(new Runnable() 
		{
			public void run() 
			{
				new JavaClient().init_socket();				
			}
		});			
	}	
}
