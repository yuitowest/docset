#! /bin/bash

database_path='./erlang.docset/Contents/Resources/docSet.dsidx'
documents_path='./erlang.docset/Contents/Resources/Documents'

rm -f ${database_path}
rm -rf ${documents_path}
mkdir -p ${documents_path}
curl -L -O http://www.erlang.org/download/otp_doc_html_R16B03-1.tar.gz
tar zxf otp_doc_html_R16B03-1.tar.gz -C ${documents_path}
cp ${documents_path}/doc/erlang-logo.png ./erlang.docset/icon.png
cp ./otp_doc.css ${documents_path}/doc/otp_doc.css
