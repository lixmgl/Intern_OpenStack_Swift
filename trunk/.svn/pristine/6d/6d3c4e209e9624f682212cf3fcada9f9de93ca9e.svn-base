
import java.sql.Time;
import java.util.Date;
import java.util.Iterator;

import java.util.Properties;
import org.jclouds.Constants;
import org.jclouds.blobstore.BlobStore;
import org.jclouds.blobstore.BlobStoreContext;
import org.jclouds.blobstore.BlobStoreContextFactory;
import org.jclouds.blobstore.domain.BlobBuilder;
import org.jclouds.blobstore.domain.PageSet;
import org.jclouds.blobstore.domain.StorageMetadata;

import org.jclouds.blobstore.util.BlobStoreUtils;
import org.jclouds.enterprise.config.EnterpriseConfigurationModule;

import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Iterables;
import com.google.inject.Module;

public class JCloudClient {
	

	private static BlobStoreContext context;
	
	public JCloudClient(String endPoint, String identity, String credential, String provider){
		if (!Iterables.contains(BlobStoreUtils.getSupportedProviders(), provider))
	         throw new IllegalArgumentException("provider " + provider + " not in supported list: "
	                  + BlobStoreUtils.getSupportedProviders());
		
		Properties overrides = new Properties();
		overrides.setProperty("swift.endpoint", endPoint);
		overrides.setProperty(Constants.PROPERTY_TRUST_ALL_CERTS, "true"); 
		overrides.setProperty(Constants.PROPERTY_RELAX_HOSTNAME, "true"); 

		context = (new BlobStoreContextFactory()).createContext(provider,
				identity, credential, ImmutableSet.<Module>of(new EnterpriseConfigurationModule()), overrides);
		
	}
	
	public void close(){
		if (context != null){
			context.close();
		}
	}
	
	public void listContainers(){
		
		BlobStore blobStore = context.getBlobStore();
		PageSet metadataSet = blobStore.list();
		Iterator iterator = metadataSet.iterator();
		while(iterator.hasNext()){
			StorageMetadata metadata = (StorageMetadata) iterator.next();
			System.out.println(String.format("%s : %s", metadata.getType(), metadata.getName()));
		}
	}
	
	public void listObjects(String container){
	
		BlobStore blobStore = context.getBlobStore();
		PageSet metadataSet = blobStore.list(container);
		Iterator iterator = metadataSet.iterator();
		while(iterator.hasNext()){
			StorageMetadata metadata = (StorageMetadata) iterator.next();
			System.out.println(String.format("%s : %s", metadata.getType(), metadata.getName()));
		}
		
	}
	
	public boolean createContainer(String container){
		BlobStore blobStore = context.getBlobStore();
		return blobStore.createContainerInLocation(null, container);
	}
	public String createObject(String container, String object){
		BlobStore blobStore = context.getBlobStore();
		BlobBuilder builder = blobStore.blobBuilder(object);
		builder.payload("Hello world!");
		return blobStore.putBlob(container, builder.build());
	}
	
	public static void main(String [] args){
		//String endPoint = "http://10.100.32.36:5000/v1.0";
		String endPoint = "https://10.100.18.149:5000";
		String identity = "admin";
		String credential = "secrete";
		String provider = "swift";
		JCloudClient client = null;
		
		Date beginDate = new Date();
		try{
			client = new JCloudClient(endPoint, identity, credential, provider);
			client.createContainer("autumn");
			
			
			client.createContainer("test2");
			
			String etagString = client.createObject("test2", "file1.txt");
			if (etagString != null)
				System.out.println("Created file file1.txt [etag = " + etagString+"]");
			
			client.listContainers();
			client.listObjects("test2");
			
		}finally{
			client.close();
		}
		
		Date endDate = new Date();
		System.out.println("Interval = " + (endDate.getTime() - beginDate.getTime()));
	}

}
