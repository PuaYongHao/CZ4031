import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.time.LocalTime;
import java.util.*;

import Storage.Address;
import Storage.Disk;
import Storage.Record;
import Index.BPlusTree;
//import app.util.Log;
//import app.util.Utility;

public class MainApp {
	// private static final String TAG = "App";
	Scanner scanner = new Scanner(System.in);
	private Disk disk;
	private BPlusTree index;

	//experiment 5 variable
	private Disk experiment5Disk;
	private BPlusTree experiment5Index;


	public void run(int blockSize) throws Exception {
		// read records from data file
		List<Record> records = readRecord("data.tsv");

		disk = new Disk(500 * 1024 * 1024, blockSize);
		index = new BPlusTree(blockSize);
		experiment5Disk = new Disk(500*1024*1024, blockSize);
		experiment5Index = new BPlusTree(blockSize);
		
		System.out.println("Block size: " + blockSize);
		Address recordAddr;
		Address recordAddrExperiment5;
		for (Record r: records) {
			// inserting records into disk and create index!
			recordAddr = disk.appendRecord(r);
			index.insert( r.getNumVotes(), recordAddr);
			recordAddrExperiment5 = experiment5Disk.appendRecord(r);
			experiment5Index.insert( r.getNumVotes(), recordAddrExperiment5);
		}


		//index.treeStats();

		// TODO do experiences
		pause("\nPress enter for experiment 1...");
		experiment1(records, blockSize);
		pause("\nPress enter for experiment 2...");
		experiment2();
		pause("\nPress enter for experiment 3...");
		experiment3();
		pause("\nPress enter for experiment 4...");
		experiment4();
		pause("\nPress enter for experiment 5...");
		experiment5();
		System.out.println("\nEnd of experiment...");
	}

	public void experiment1(List<Record> records, int blockSize) {
		System.out.println("Starting Experiment 1......");
		System.out.println("Total number of records: " + records.size());
		System.out.println("The size of a record: " + Record.size());
		System.out.println("The number of records stored in a block: " + blockSize / Record.size());
		System.out.println("The number of blocks for storing the data: " + disk.getBlocksCount());
	}

	public void experiment2() {
		System.out.println("Starting Experiment 2......");
		index.treeStats();
	}

	public void experiment3() {
		System.out.println("Starting Experiment 3......");
		System.out.println("Search for numVotes == 500 ......");

		// normal B+ scanning
		LocalTime timeStart = LocalTime.now(); // record start time
		ArrayList<Address> exp3Record = index.getRecordsWithKey(500);
		// retrieve all the actual records inside the block
		ArrayList<Record> records = disk.getRecords(exp3Record);
		LocalTime timeEnd = LocalTime.now(); // record end time
		printTime(timeStart.toString(),timeEnd.toString());

		// bruteforce way
		timeStart = LocalTime.now();
		ArrayList<Record> recordsByBF = disk.getRecordsByBruteForce(500);
		timeEnd = LocalTime.now();
		printTime(timeStart.toString(),timeEnd.toString());
		
		
		double averageRating = 0;
		for (Record record : records) {
			averageRating += record.getAvgRating();
		}
		averageRating /= records.size();
		System.out.println("Average rating of movies with numVotes == 500 is: " + averageRating);
	}

	public void experiment4() {
		// Log.i(TAG,"Experience 4 started, getting records with numVotes between
		// 30k-40k ");
		LocalTime timeStart = LocalTime.now(); // record start time
		ArrayList<Address> exp4Record = index.getRecordsWithKeyInRange(30000, 40000);
		ArrayList<Record> records = disk.getRecords(exp4Record);
		LocalTime timeEnd = LocalTime.now(); // record end time
		printTime(timeStart.toString(),timeEnd.toString());
		
		//bruteforce
		timeStart = LocalTime.now();
		ArrayList<Record> recordsByBF = disk.getRecordsByBruteForce(30000,40000);
		timeEnd = LocalTime.now();
		printTime(timeStart.toString(),timeEnd.toString());
		
		// records collected, do calculate average rating
		double averageRating = 0;
		for (Record record : records) {
			averageRating += record.getAvgRating();
		}
		averageRating /= records.size();
		System.out.println("Average rating of movies with numVotes between 30,000 and 40,000 is: " + averageRating);
	}

	public void experiment5() {
		System.out.println("Starting Experiment 5.............");
		LocalTime timeStart = LocalTime.now(); // record start time
		index.deleteKey(1000);
		LocalTime timeEnd = LocalTime.now(); // record end time
		printTime(timeStart.toString(),timeEnd.toString());
		
		// bruteforce
		timeStart = LocalTime.now(); // record start time
		experiment5Disk.deleteRecordsByBruteForce(1000);
		timeEnd = LocalTime.now(); // record end time
		printTime(timeStart.toString(),timeEnd.toString());
	}
	
	private void printTime(String start, String end) {
		System.out.println("Start time: "+start+" End time: "+end);
		Double timeTaken = Double.parseDouble(end.toString().substring(end.toString().lastIndexOf(":")+1)) - Double.parseDouble(start.toString().substring(start.toString().lastIndexOf(":")+1));
		System.out.println("Time taken: "+ timeTaken+ "s\n");
	}

	private void pause(String message) {
		if (message == null) {
			message = "Press any key to continue";
		}
		System.out.print(message);
		scanner.nextLine();
	}

	private List<Record> readRecord(String path) throws Exception {
		File dataFile = new File(path);
		if (!dataFile.exists()) {
			System.out.println("File does not exist... re-reading the file now...");

			dataFile = new File("Database/src", path);
			if (!dataFile.exists()) {
				throw new FileNotFoundException("File not exist");
			}
		}

		BufferedReader br = null;
		List<Record> records = new ArrayList<>();
		String line;
		String[] parts = null;
		try {
			br = new BufferedReader(new FileReader(dataFile));
			// reading header first (to be skipped)
			br.readLine();
			while ((line = br.readLine()) != null) {
				parts = line.split("\\t");
				Record record = new Record(parts[0], Float.parseFloat(parts[1]), Integer.parseInt(parts[2]));
				records.add(record);
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					System.out.println(e.getMessage());
				}
			}
		}
		// System.out.println("Total records: " + records.size());
		return records;
	}

	public static void main(String[] args) {
		try {
			MainApp app = new MainApp();
			app.run(200);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
