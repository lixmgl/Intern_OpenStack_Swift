package cisco.jcloudsapi;

import java.io.IOException;
import java.io.InputStream;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Properties;
import java.util.Set;

import javax.annotation.Resource;

import org.jboss.netty.handler.codec.http.HttpHeaders.Values;
import org.jclouds.Constants;
import org.jclouds.blobstore.BlobStoreContext;
import org.jclouds.blobstore.BlobStoreContextFactory;
import org.jclouds.blobstore.domain.PageSet;
import org.jclouds.enterprise.config.EnterpriseConfigurationModule;
import org.jclouds.http.internal.JavaUrlHttpCommandExecutorService;
import org.jclouds.io.Payload;
import org.jclouds.logging.Logger;
import org.jclouds.openstack.swift.SwiftAsyncClient;
import org.jclouds.openstack.swift.SwiftClient;
import org.jclouds.openstack.swift.domain.ContainerMetadata;
import org.jclouds.openstack.swift.domain.MutableObjectInfoWithMetadata;
import org.jclouds.openstack.swift.domain.ObjectInfo;
import org.jclouds.openstack.swift.domain.SwiftObject;
import org.jclouds.openstack.swift.domain.internal.MutableObjectInfoWithMetadataImpl;
import org.jclouds.openstack.swift.domain.internal.SwiftObjectImpl;
import org.jclouds.rest.RestContext;

import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Multimap;
import com.google.inject.Module;
import com.sun.jersey.spi.StringReader.ValidateDefaultValue;

/**
 * 
 */



/**
 * @author autumn
 * Demo class for Jclouds swift API.
 */
public class JcloudSwiftAPIDemo {

	private static BlobStoreContext context = null;
	private static SwiftClient swiftClient = null;
		
	/**
	 * 
	 * @param endPoint
	 * @param user
	 * @param passwd
	 */
	public JcloudSwiftAPIDemo(String endPoint, String user, String passwd){
		Properties overrides = new Properties();
		
		overrides.setProperty("swift.endpoint", endPoint);
		overrides.setProperty(Constants.PROPERTY_TRUST_ALL_CERTS, "true"); 
		overrides.setProperty(Constants.PROPERTY_RELAX_HOSTNAME, "true"); 
		

		this.context = (new BlobStoreContextFactory()).createContext("swift",
		user, passwd, ImmutableSet.<Module>of(new EnterpriseConfigurationModule()), overrides);
		
		RestContext<SwiftClient, SwiftAsyncClient> providerContext = context.getProviderSpecificContext();
		this.swiftClient =  providerContext.getApi();
				
	}
	
	/**
	 * Close the connection to swift proxy server
	 */
	public void close(){
		this.context.close();
	}
	
	/**
	 * List all containers under the user
	 */
	public void listContainers(){
		Set<ContainerMetadata> containers = this.swiftClient.listContainers();
        Iterator<ContainerMetadata> iterator = containers.iterator();
        System.out.println("**********************************************************************************");
        System.out.println(String.format("There are totally %d container(s) in current swift boject store:", containers.size()));
        System.out.println("**********************************************************************************");
        while(iterator.hasNext()){
        	ContainerMetadata metadata = iterator.next();
        	System.out.println("[Container] " + metadata.getName());
        }
		
	}
	
	/**
	 * 
	 * @param container
	 * @throws IOException
	 */
	public void listObjectsOfContainer(String container) throws IOException{
		PageSet<ObjectInfo> objectInfos = this.swiftClient.listObjects(container);
    	Iterator<ObjectInfo> it = objectInfos.iterator();
    	System.out.println("**********************************************************************************");
        System.out.println(String.format("There are totally %d object(s) in container %s:", objectInfos.size(), container));
        System.out.println("**********************************************************************************");
    	while(it.hasNext()){
    		ObjectInfo obj = it.next();
    		System.out.println(String.format("[Object] %s <%d bytes>", obj.getName(), obj.getBytes().longValue()));
    		SwiftObject swiftObject = this.swiftClient.getObject(container, obj.getName());
    		Payload payload = swiftObject.getPayload();
    		InputStream in = payload.getInput();
    		byte [] buff = new byte[1024];
    		in.read(buff);
    		String content = new String(buff);
    		//System.out.println("  content : " + content);
    	}
	}
	
	
	/**
	 * 
	 * @param container
	 * @return
	 */
	public boolean createContainer(String container){
		boolean ret = this.swiftClient.createContainer(container);
		System.out.println("Created container-------" + container);
		return ret;
	}
	
	/**
	 * 
	 * @param container
	 * @return
	 */
	public boolean removeContainer(String container){
		PageSet<ObjectInfo> objs = this.swiftClient.listObjects(container);
		Iterator<ObjectInfo> it = objs.iterator();
		while(it.hasNext()){
        	ObjectInfo info = it.next();
        	String name = info.getName();
        	this.removeObject(container, name);
        }
		
		boolean ret =  this.swiftClient.deleteContainerIfEmpty(container);
		System.out.println("Removed container-------" + container);
		return ret;
	}
	
	/**
	 * Create a object under container
	 * @param container
	 * @param objName
	 * @param payload
	 * @return
	 */
	public String createObject(String container, String objName, String payload){
		MutableObjectInfoWithMetadata meta = new MutableObjectInfoWithMetadataImpl();
		meta.setContainer(container);
		meta.setName(objName);
		
		SwiftObject object = new SwiftObjectImpl(meta);
		object.setPayload(payload);
		
		String retString = this.swiftClient.putObject(container, object);
		System.out.println("  Created object-------" + container + "/" + objName);
		return retString;
	}
	
	
	/**
	 * Remove a object
	 * @param container
	 * @param objName
	 */
	public void removeObject(String container, String objName){
		this.swiftClient.removeObject(container, objName);
		System.out.println("  Removed object-------" + container + "/" + objName);
	}
	
	/**
	 * Create lots of containers and objects, for stress testing
	 * @param containerBaseName
	 * @param objBaseName
	 * @param containerNum
	 * @param objNum
	 */
	public void createContainerAndObjects(String containerBaseName, String objBaseName, int containerNum, int objNum){
		for (int i = 0; i < containerNum; i++){
			String container = containerBaseName + "-" + i;
			if (swiftClient.containerExists(container) == false){
				this.createContainer(container);
			}
			for (int j = 0; j < objNum; j ++ ){
				String obj = objBaseName + "-" + j;
				if (swiftClient.objectExists(container, obj) == false){
					this.createObject(container, obj, "Just for testing........");
				}
			}
		}
	}
	
	/**
	 * Reverse operation of createContainerAndObjects, for stress testing
	 * @param container
	 * @param conNum
	 */
	public void removeContainers(String container, int conNum) {
		for (int i = 0; i < conNum; i ++ ){
			String conName = container + "-" + i;
			if (swiftClient.containerExists(conName)){
				this.removeContainer(conName);
			}
		}
	}
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		System.err.close();
		
		//String endPoint = "http://10.100.32.36:5000/v1.0";
		String endPoint = "https://10.100.18.149:5000/v1.0";
		String user = "admin";
		String passwd = "secrete";
				
		JcloudSwiftAPIDemo client = new JcloudSwiftAPIDemo(endPoint, user, passwd);
		
		try{
			
			client.createContainer("test1");
			client.createObject("test1", "obj1", "Hello world!");
			client.listContainers();
			client.listObjectsOfContainer("test1");	
		}catch (Exception e){
			System.out.println("Error : " + e.getMessage());
		}finally{
			client.close();
		}
	
		/*
		if (args.length < 5 || args.length > 9){
			System.out.println("Usage : java JcloudSwiftClient server port user passwd list-containers");
			System.out.println("        java JcloudSwiftClient server port user passwd list-objects container");
			System.out.println("        java JcloudSwiftClient server port user passwd create-container container");
			System.out.println("        java JcloudSwiftClient server port user passwd remove-container container");
			System.out.println("        java JcloudSwiftClient server port user passwd create-object container object");
			System.out.println("        java JcloudSwiftClient server port user passwd remove-object container object");
			System.out.println("        java JcloudSwiftClient server port user passwd create-objects container object number");
			System.out.println("        java JcloudSwiftClient server port user passwd create-con-objs containerBaseName objBaseName conNumber objNum");
			System.out.println("        java JcloudSwiftClient server port user passwd remove-containers containerBaseName conNumber");
			System.exit(0);
		}
		
		System.err.close();
		
		String server = args[0];
		int port = Integer.valueOf(args[1]);
		String user = args[2];
		String passwd = args[3];
		String command = args[4];
				
		JcloudSwiftClient client = new JcloudSwiftClient(server, port, user, passwd);
		try{
			if(command.equals("list-containers")){
				client.listContainers();
			}else if (command.equals("list-objects")){
				String container = args[5];
				client.listObjectsOfContainer(container);
			}else if(command.equals("create-container")){
				String container = args[5];
				client.createContainer(container);
			}else if(command.equals("remove-container")){
				String container = args[5];
				client.removeContainer(container);
			}
			else if (command.equals("create-object")){
				String container = args[5];
				String objName = args[6];
				client.createObject(container, objName, "Just for testing!");
			}else if (command.equals("create-objects")){
				String container = args[5];
				String objName = args[6];
				int numOfObjs = Integer.valueOf(args[7]);
				for (int i = 0; i < numOfObjs; i++){
					objName += String.format("%s-%3d", objName, i);
					client.createObject(container, objName, "Just for testing!");
				}
			}
			else if (command.equals("remove-object")){
				String container = args[5];
				String objName = args[6];
				client.removeObject(container, objName);
			}
			else if (command.equals("create-con-objs")){
				String container = args[5];
				String objName = args[6];
				int conNum = Integer.valueOf(args[7]);
				int objNum = Integer.valueOf(args[8]);
				client.createContainerAndObjects(container, objName, conNum, objNum);
			}
			else if (command.equals("remove-containers")){
				String container = args[5];
				int conNum = Integer.valueOf(args[6]);
				client.removeContainers(container, conNum);
			}
			else{
				System.out.println("Unsupported command : " + command);
			}
		}catch (Exception e){
			System.out.println("Error : " + e.getMessage());
		}finally{
			client.close();
		}*/
	}
}