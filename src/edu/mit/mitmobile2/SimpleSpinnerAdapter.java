package edu.mit.mitmobile2;

import java.util.ArrayList;
import java.util.List;
import java.util.zip.Inflater;

import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.AbsListView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;

public class SimpleSpinnerAdapter extends ArrayAdapter<String> {
	
	protected String mTitle;
	protected List<String> mValues;
	protected Context mContext;
	private View mEmptyView;
	
	private static List<String> combineTitleAndValues(String title, List<String> values) {
		ArrayList<String> allStrings = new ArrayList<String>();
		allStrings.add(title);
		allStrings.addAll(values);
		return allStrings;
	}
	
	public SimpleSpinnerAdapter(Context context, String title, List<String> values) {
		super(context, android.R.layout.simple_spinner_item, combineTitleAndValues(title, values));
		mContext = context;
		mTitle = title;
		mValues = values;
	}
	
	public View getDropDownView(int position, View convertView, ViewGroup parent) {
		if(position == 0) {
			if(mEmptyView == null) {
				mEmptyView = new View(mContext);
				mEmptyView.setLayoutParams(new AbsListView.LayoutParams(LayoutParams.FILL_PARENT, 0));
			}
			return mEmptyView;
		}
		
		if(convertView == null || convertView == mEmptyView) {
			LayoutInflater inflator = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			convertView = inflator.inflate(R.layout.boring_action_row, null);
		}
		
		TwoLineActionRow actionRow = (TwoLineActionRow) convertView;
		actionRow.setTitle(mValues.get(position-1));
		return actionRow;
	}
	
}